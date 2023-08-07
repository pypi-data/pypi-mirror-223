import { RenderMimeRegistry, standardRendererFactories as initialFactories } from '@jupyterlab/rendermime';
import { CommandRegistry } from '@lumino/commands';
import { CodeMirrorEditorFactory, CodeMirrorMimeTypeService, EditorLanguageRegistry, EditorExtensionRegistry, EditorThemeRegistry, ybinding } from '@jupyterlab/codemirror';
import { BoxPanel } from '@lumino/widgets';
import { ConsolePanel } from '@jupyterlab/console';
class ConsoleAdapter {
    _panel;
    constructor(serviceManager) {
        this._panel = new BoxPanel();
        this._panel.direction = 'top-to-bottom';
        this._panel.spacing = 0;
        this._panel.addClass('dla-JupyterLab-Console');
        serviceManager.ready.then(() => {
            this.startConsole('console-path', serviceManager, this._panel);
        });
    }
    startConsole(path, serviceManager, panel) {
        const commands = new CommandRegistry();
        document.addEventListener('keydown', event => {
            commands.processKeydownEvent(event);
        });
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
        const factoryService = new CodeMirrorEditorFactory({
            extensions: editorExtensions(),
            languages
        });
        const rendermime = new RenderMimeRegistry({ initialFactories });
        const mimeTypeService = new CodeMirrorMimeTypeService(languages);
        const editorFactory = factoryService.newInlineEditor;
        const contentFactory = new ConsolePanel.ContentFactory({ editorFactory });
        const consolePanel = new ConsolePanel({
            manager: serviceManager,
            rendermime,
            path,
            contentFactory,
            mimeTypeService,
            kernelPreference: {
                shouldStart: true,
                name: 'python',
                //        autoStartDefault: true,
            }
        });
        consolePanel.title.label = 'Console';
        BoxPanel.setStretch(consolePanel, 1);
        panel.addWidget(consolePanel);
        window.addEventListener('resize', () => {
            panel.update();
        });
        const selector = '.jp-ConsolePanel';
        let command;
        command = 'console:clear';
        commands.addCommand(command, {
            label: 'Clear',
            execute: () => {
                consolePanel.console.clear();
            }
        });
        command = 'console:execute';
        commands.addCommand(command, {
            label: 'Execute Prompt',
            execute: () => {
                return consolePanel.console.execute();
            }
        });
        commands.addKeyBinding({ command, selector, keys: ['Enter'] });
        command = 'console:execute-forced';
        commands.addCommand(command, {
            label: 'Execute Cell (forced)',
            execute: () => {
                return consolePanel.console.execute(true);
            }
        });
        commands.addKeyBinding({ command, selector, keys: ['Shift Enter'] });
        command = 'console:linebreak';
        commands.addCommand(command, {
            label: 'Insert Line Break',
            execute: () => {
                consolePanel.console.insertLinebreak();
            }
        });
        commands.addKeyBinding({ command, selector, keys: ['Ctrl Enter'] });
    }
    get panel() {
        return this._panel;
    }
}
export default ConsoleAdapter;
//# sourceMappingURL=ConsoleAdapter.js.map