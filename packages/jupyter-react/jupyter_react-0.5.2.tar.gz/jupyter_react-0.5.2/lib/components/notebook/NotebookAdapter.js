import { CommandRegistry } from '@lumino/commands';
import { BoxPanel, Widget } from '@lumino/widgets';
import { DocumentRegistry, Context } from '@jupyterlab/docregistry';
import { standardRendererFactories, RenderMimeRegistry } from '@jupyterlab/rendermime';
import { rendererFactory as jsonRendererFactory } from '@jupyterlab/json-extension';
import { rendererFactory as javascriptRendererFactory } from '@jupyterlab/javascript-extension';
import { NotebookPanel, NotebookWidgetFactory, NotebookTracker, NotebookActions } from '@jupyterlab/notebook';
import { CodeMirrorEditorFactory, CodeMirrorMimeTypeService, EditorLanguageRegistry, EditorExtensionRegistry, EditorThemeRegistry, ybinding } from '@jupyterlab/codemirror';
import { Completer, CompleterModel, CompletionHandler, ProviderReconciliator, KernelCompleterProvider } from '@jupyterlab/completer';
import { MathJaxTypesetter } from '@jupyterlab/mathjax-extension';
import { requireLoader } from "@jupyter-widgets/html-manager";
import { WIDGET_MIMETYPE, WidgetRenderer } from "@jupyter-widgets/html-manager/lib/output_renderers";
import JupyterReactContentFactory from './content/JupyterReactContentFactory';
import JupyterReactNotebookModelFactory from './model/JupyterReactNotebookModelFactory';
import { NotebookCommands } from './NotebookCommands';
import { IPyWidgetsClassicManager } from "./../../jupyter/ipywidgets/IPyWidgetsClassicManager";
import { activateWidgetExtension } from "./../../jupyter/ipywidgets/IPyWidgetsJupyterLabPlugin";
import getMarked from './marked/marked';
// import { activatePlotlyWidgetExtension } from "./../../jupyter/ipywidgets/plotly/JupyterlabPlugin";
export class NotebookAdapter {
    _boxPanel;
    _notebookPanel;
    _uid;
    _serviceManager;
    _commandRegistry;
    _path;
    _nbformat;
    _tracker;
    _kernel;
    _store;
    _ipywidgets;
    _iPyWidgetsClassicManager;
    _CellSidebar;
    _nbgrader;
    //  private _readOnly: boolean;
    _context;
    _renderers;
    _rendermime;
    constructor(props, store, serviceManager) {
        this._path = props.path;
        this._store = store;
        this._serviceManager = serviceManager;
        this._nbformat = props.nbformat;
        this._CellSidebar = props.CellSidebar;
        this._nbgrader = props.nbgrader;
        //    this._readOnly = props.readOnly;
        this._ipywidgets = props.ipywidgets;
        this._kernel = props.kernel;
        this._uid = props.uid;
        this._renderers = props.renderers;
        this._boxPanel = new BoxPanel();
        this._boxPanel.addClass('dla-Jupyter-Notebook');
        this._boxPanel.spacing = 0;
        this._commandRegistry = new CommandRegistry();
        //    this.loadNotebook = this.loadNotebook.bind(this);
        this.loadNotebook();
    }
    loadNotebook() {
        const useCapture = true;
        document.addEventListener('keydown', event => { this._commandRegistry?.processKeydownEvent(event); }, useCapture);
        const rendererFactories = standardRendererFactories.filter(factory => factory.mimeTypes[0] !== 'text/javascript');
        rendererFactories.push(jsonRendererFactory);
        rendererFactories.push(javascriptRendererFactory);
        this._renderers.map(renderer => rendererFactories.push(renderer));
        const languages = new EditorLanguageRegistry();
        // Register default languages.
        for (const language of EditorLanguageRegistry.getDefaultLanguages()) {
            languages.addLanguage(language);
        }
        // Add Jupyter Markdown flavor here to support code block highlighting.
        languages.addLanguage({
            name: 'ipythongfm',
            mime: 'text/x-ipythongfm',
            load: async () => {
                // TODO: add support for LaTeX
                const m = await import('@codemirror/lang-markdown');
                return m.markdown({
                    codeLanguages: (info) => languages.findBest(info)
                });
            }
        });
        this._rendermime = new RenderMimeRegistry({
            initialFactories: rendererFactories,
            latexTypesetter: new MathJaxTypesetter(),
            markdownParser: getMarked(languages),
        });
        const documentRegistry = new DocumentRegistry({});
        const mimeTypeService = new CodeMirrorMimeTypeService(languages);
        const themes = new EditorThemeRegistry();
        for (const theme of EditorThemeRegistry.getDefaultThemes()) {
            themes.addTheme(theme);
        }
        const editorExtensions = () => {
            const registry = new EditorExtensionRegistry();
            for (const extensionFactory of EditorExtensionRegistry.getDefaultExtensions({ themes })) {
                registry.addExtension(extensionFactory);
            }
            registry.addExtension({
                name: 'shared-model-binding',
                factory: options => {
                    const sharedModel = options.model.sharedModel;
                    return EditorExtensionRegistry.createImmutableExtension(ybinding({
                        ytext: sharedModel.ysource,
                        undoManager: sharedModel.undoManager ?? undefined
                    }));
                }
            });
            return registry;
        };
        const factoryService = new CodeMirrorEditorFactory({
            extensions: editorExtensions(),
            languages
        });
        const editorServices = {
            factoryService,
            mimeTypeService,
        };
        const editorFactory = editorServices.factoryService.newInlineEditor;
        const contentFactory = this._CellSidebar
            ?
                new JupyterReactContentFactory(this._CellSidebar, this._uid, this._nbgrader, this._commandRegistry, { editorFactory }, this._store)
            :
                new NotebookPanel.ContentFactory({ editorFactory });
        this._tracker = new NotebookTracker({ namespace: this._uid });
        switch (this._ipywidgets) {
            case 'classic': {
                this._iPyWidgetsClassicManager = new IPyWidgetsClassicManager({ loader: requireLoader });
                this._rendermime.addFactory({
                    safe: false,
                    mimeTypes: [WIDGET_MIMETYPE],
                    createRenderer: (options) => new WidgetRenderer(options, this._iPyWidgetsClassicManager),
                }, 1);
                break;
            }
            case 'lab': {
                const widgetRegistry = activateWidgetExtension(this._rendermime, this._tracker, null, null);
                console.log('Widget Registry', widgetRegistry);
                //        activatePlotlyWidgetExtension(widgetRegistry);
                break;
            }
        }
        const notebookWidgetFactory = new NotebookWidgetFactory({
            name: 'Notebook',
            modelName: 'notebook',
            fileTypes: ['notebook'],
            defaultFor: ['notebook'],
            preferKernel: true,
            canStartKernel: false,
            rendermime: this._rendermime,
            contentFactory,
            mimeTypeService: editorServices.mimeTypeService,
        });
        notebookWidgetFactory.widgetCreated.connect((sender, notebookPanel) => {
            notebookPanel.context.pathChanged.connect(() => {
                void this._tracker?.save(notebookPanel);
            });
            void this._tracker?.add(notebookPanel);
        });
        documentRegistry.addWidgetFactory(notebookWidgetFactory);
        const notebookModelFactory = new JupyterReactNotebookModelFactory({
            nbformat: this._nbformat,
        });
        documentRegistry.addModelFactory(notebookModelFactory);
        this._context = new Context({
            manager: this._serviceManager,
            factory: notebookModelFactory,
            path: this._path || "ping.ipynb",
            kernelPreference: {
                //        id: this.kernel?.kernelId,
                shouldStart: false,
                autoStartDefault: false,
                shutdownOnDispose: false,
            }
        });
        /*
        const content = new Notebook({
          rendermime: this._rendermime,
          contentFactory,
          mimeTypeService,
          notebookConfig: {
            ...StaticNotebook.defaultNotebookConfig,
            windowingMode: 'none'
          }
        });
        this._notebookPanel = new NotebookPanel({
          context: this._context,
          content,
        })
        */
        this._notebookPanel = documentRegistry.getWidgetFactory('Notebook')?.createNew(this._context);
        if (this._ipywidgets === 'classic') {
            this._notebookPanel.sessionContext.kernelChanged.connect((sender, args) => {
                this._iPyWidgetsClassicManager?.registerWithKernel(args.newValue);
            });
        }
        const isNew = ((this._path !== undefined) && (this._path !== "")) ? false : true;
        this._context.initialize(isNew).then(() => {
            if (this._kernel) {
                //     this._kernel.getJupyterKernel().then(kernelConnection => {
                this.changeKernel(this._kernel);
                //     });
            }
        });
        BoxPanel.setStretch(this._notebookPanel, 0);
        this._boxPanel.addWidget(this._notebookPanel);
        window.addEventListener('resize', () => {
            this._notebookPanel?.update();
        });
        //    const tracker = this._tracker;
        function getCurrent(args) {
            //      const widget = tracker.currentWidget;
            return this._tracker.currentWidget;
        }
        function isEnabled() {
            return (
            //        this._tracker.currentWidget !== null
            this._tracker.currentWidget !== null);
        }
        this._commandRegistry.addCommand('run-selected-codecell', {
            label: 'Run Cell',
            execute: args => {
                const current = getCurrent(args);
                if (current) {
                    const { context, content } = current;
                    NotebookActions.run(content, context.sessionContext);
                }
            },
            isEnabled,
        });
    }
    setNbformat(nbformat) {
        this._nbformat = nbformat;
        if (this._nbformat) {
            this._notebookPanel?.model?.fromJSON(nbformat);
        }
    }
    setupCompleter(notebookPanel) {
        const editor = notebookPanel.content.activeCell && notebookPanel.content.activeCell.editor;
        const sessionContext = notebookPanel.context.sessionContext;
        const completerModel = new CompleterModel();
        const completer = new Completer({ editor, model: completerModel });
        const completerTimeout = 1000;
        const provider = new KernelCompleterProvider();
        const reconciliator = new ProviderReconciliator({
            context: {
                widget: notebookPanel,
                editor,
                session: sessionContext.session
            },
            providers: [provider],
            timeout: completerTimeout,
        });
        const handler = new CompletionHandler({ completer, reconciliator });
        void sessionContext.ready.then(() => {
            const provider = new KernelCompleterProvider();
            const reconciliator = new ProviderReconciliator({
                context: { widget: this._notebookPanel, editor, session: sessionContext.session },
                providers: [provider],
                timeout: completerTimeout,
            });
            handler.reconciliator = reconciliator;
        });
        handler.editor = editor;
        notebookPanel.content.activeCellChanged.connect((sender, snippet) => {
            handler.editor = snippet && snippet.editor;
        });
        completer.hide();
        Widget.attach(completer, document.body);
        return handler;
    }
    changeKernel(kernel) {
        this._kernel = kernel;
        this._kernel.connection.then(kernelConnection => {
            this._context?.sessionContext.changeKernel(kernelConnection.model).then(() => {
                const completerHandler = this.setupCompleter(this._notebookPanel);
                NotebookCommands(this._commandRegistry, this._notebookPanel, completerHandler, this._path);
                this._iPyWidgetsClassicManager?.registerWithKernel(kernelConnection);
                //        const widgetRegistry = activateWidgetExtension(this._rendermime!, this._tracker!, null, null);
                //        activatePlotlyWidgetExtension(widgetRegistry);    
            });
        });
    }
    get uid() {
        return this._uid;
    }
    get notebookPanel() {
        return this._notebookPanel;
    }
    get commands() {
        return this._commandRegistry;
    }
    get panel() {
        return this._boxPanel;
    }
    get serviceManager() {
        return this._serviceManager;
    }
    setDefaultCellType = (cellType) => {
        this._notebookPanel.content.notebookConfig.defaultCell = cellType;
    };
    changeCellType = (cellType) => {
        //    NotebookActions.changeCellType(this._notebookPanel?.content!, cellType);
        this.doChangeCellType(this._notebookPanel?.content, cellType);
    };
    doChangeCellType(notebook, value) {
        const notebookSharedModel = notebook.model.sharedModel;
        notebook.widgets.forEach((child, index) => {
            if (!notebook.isSelectedOrActive(child)) {
                return;
            }
            if (child.model.type !== value) {
                const raw = child.model.toJSON();
                notebookSharedModel.transact(() => {
                    notebookSharedModel.deleteCell(index);
                    const newCell = notebookSharedModel.insertCell(index, {
                        cell_type: value,
                        source: raw.source,
                        metadata: raw.metadata
                    });
                    if (raw.attachments && ['markdown', 'raw'].includes(value)) {
                        newCell.attachments =
                            raw.attachments;
                    }
                });
            }
            if (value === 'markdown') {
                // Fetch the new widget and unrender it.
                child = notebook.widgets[index];
                child.rendered = false;
            }
        });
        notebook.deselectAll();
    }
    dispose = () => {
        //    this._context?.dispose();
        //    this._notebookPanel?.dispose();
    };
}
export default NotebookAdapter;
//# sourceMappingURL=NotebookAdapter.js.map