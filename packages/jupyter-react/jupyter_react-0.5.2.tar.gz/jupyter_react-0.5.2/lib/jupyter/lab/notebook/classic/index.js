import { ILayoutRestorer } from '@jupyterlab/application';
import { ICommandPalette, WidgetTracker, ToolbarButton } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { INotebookTracker } from '@jupyterlab/notebook';
import { INotebookRenderTracker, ClassicRenderFactory } from './classic';
import { notebookClassicIcon } from './icons';
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.classicRender = 'notebook:render-with-classic';
    CommandIDs.classicOpen = 'notebook:open-with-classic';
})(CommandIDs || (CommandIDs = {}));
const WIDGET_FACTORY = 'Classic Render';
class NotebookPreviewButton {
    _commands;
    constructor(commands) {
        this._commands = commands;
    }
    createNew(panel) {
        const button = new ToolbarButton({
            className: 'classicRender',
            tooltip: 'Render with Classic',
            icon: notebookClassicIcon,
            onClick: () => { this._commands.execute(CommandIDs.classicRender); }
        });
        panel.toolbar.insertAfter('cellType', 'classicRender', button);
        return button;
    }
}
/**
 * Initialization data for the jupyterlab-preview extension.
 */
const notebookClassicPlugin = {
    id: '@datalayer/jupyter-react:classic',
    autoStart: true,
    requires: [INotebookTracker],
    optional: [ICommandPalette, ILayoutRestorer, IMainMenu, ISettingRegistry],
    provides: INotebookRenderTracker,
    activate: (app, notebookTracker, palette, restorer, menu, settingRegistry) => {
        const { commands, docRegistry } = app;
        const tracker = new WidgetTracker({
            namespace: 'classic-preview'
        });
        if (restorer) {
            restorer.restore(tracker, {
                command: 'docmanager:open',
                args: panel => ({
                    path: panel.context.path,
                    factory: classicFactory.name
                }),
                name: panel => panel.context.path,
                when: app.serviceManager.ready
            });
        }
        function getCurrent(args) {
            const widget = notebookTracker.currentWidget;
            const activate = args['activate'] !== false;
            if (activate && widget) {
                app.shell.activateById(widget.id);
            }
            return widget;
        }
        function isEnabled() {
            return (notebookTracker.currentWidget !== null &&
                notebookTracker.currentWidget === app.shell.currentWidget);
        }
        function getPreviewUrl(path) {
            const baseUrl = PageConfig.getBaseUrl();
            return `${baseUrl}tree/${path}`;
        }
        const classicFactory = new ClassicRenderFactory(getPreviewUrl, {
            name: WIDGET_FACTORY,
            fileTypes: ['notebook'],
            modelName: 'notebook'
        });
        classicFactory.widgetCreated.connect((sender, widget) => {
            widget.context.pathChanged.connect(() => {
                void tracker.save(widget);
            });
            void tracker.add(widget);
        });
        const updateSettings = (settings) => {
            classicFactory.defaultRenderOnSave = settings.get('renderOnSave')
                .composite;
        };
        if (settingRegistry) {
            Promise.all([settingRegistry.load(notebookClassicPlugin.id), app.restored])
                .then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(updateSettings);
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        commands.addCommand(CommandIDs.classicRender, {
            label: 'Render Notebook with Classic',
            execute: async (args) => {
                const current = getCurrent(args);
                let context;
                if (current) {
                    context = current.context;
                    await context.save();
                    commands.execute('docmanager:open', {
                        path: context.path,
                        factory: WIDGET_FACTORY,
                        options: {
                            mode: 'split-right'
                        }
                    });
                }
            },
            isEnabled
        });
        commands.addCommand(CommandIDs.classicOpen, {
            label: 'Open with Classic in New Browser Tab',
            execute: async (args) => {
                const current = getCurrent(args);
                if (!current) {
                    return;
                }
                await current.context.save();
                const previewUrl = getPreviewUrl(current.context.path);
                window.open(previewUrl);
            },
            isEnabled
        });
        if (palette) {
            const category = 'Notebook Operations';
            [CommandIDs.classicRender, CommandIDs.classicOpen].forEach(command => {
                palette.addItem({ command, category });
            });
        }
        if (menu) {
            menu.viewMenu.addGroup([
                {
                    command: CommandIDs.classicRender
                },
                {
                    command: CommandIDs.classicOpen
                }
            ], 1000);
        }
        const classicRenderButton = new NotebookPreviewButton(commands);
        //
        docRegistry.addWidgetExtension('Notebook', classicRenderButton);
        docRegistry.addWidgetFactory(classicFactory);
        //
        return tracker;
    }
};
export default notebookClassicPlugin;
//# sourceMappingURL=index.js.map