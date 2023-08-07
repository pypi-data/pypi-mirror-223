import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { IFrame, ToolbarButton, ReactWidget } from '@jupyterlab/apputils';
import { ABCWidgetFactory, DocumentWidget } from '@jupyterlab/docregistry';
import { Token } from '@lumino/coreutils';
import { Signal } from '@lumino/signaling';
export const INotebookRenderTracker = new Token('@datalayer/juptyer-react:IClassicRenderTracker');
export const CLASSIC_RENDER_ICON_CLASS = 'jp-MaterialIcon jp-NotebookIcon';
export class ClassicRender extends DocumentWidget {
    _renderOnSave;
    constructor(options) {
        super({
            ...options,
            content: new IFrame({ sandbox: ['allow-same-origin', 'allow-scripts'] })
        });
        const { getPreviewUrl, context, renderOnSave } = options;
        window.onmessage = (event) => {
            //console.log("EVENT: ", event);
            switch (event.data?.level) {
                case 'debug':
                    console.debug(...event.data?.msg);
                    break;
                case 'info':
                    console.info(...event.data?.msg);
                    break;
                case 'warn':
                    console.warn(...event.data?.msg);
                    break;
                case 'error':
                    console.error(...event.data?.msg);
                    break;
                default:
                    console.log(event);
                    break;
            }
        };
        this.content.url = getPreviewUrl(context.path);
        this.content.title.iconClass = CLASSIC_RENDER_ICON_CLASS;
        this.renderOnSave = renderOnSave ? true : false;
        context.pathChanged.connect(() => {
            this.content.url = getPreviewUrl(context.path);
        });
        const reloadButton = new ToolbarButton({
            iconClass: 'jp-RefreshIcon',
            tooltip: 'Reload Preview',
            onClick: () => {
                this.reload();
            }
        });
        const renderOnSaveCheckbox = ReactWidget.create(_jsxs("label", { className: "jp-Preview-renderOnSave", children: [_jsx("input", { style: { verticalAlign: 'middle' }, name: "renderOnSave", type: "checkbox", defaultChecked: renderOnSave, onChange: (event) => {
                        this._renderOnSave = event.target.checked;
                    } }), "Render on Save"] }));
        this.toolbar.addItem('reload', reloadButton);
        if (context) {
            this.toolbar.addItem('renderOnSave', renderOnSaveCheckbox);
            void context.ready.then(() => {
                context.fileChanged.connect(() => {
                    if (this.renderOnSave) {
                        this.reload();
                    }
                });
            });
        }
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        Signal.clearData(this);
    }
    reload() {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        const iframe = this.content.node.querySelector('iframe');
        if (iframe.contentWindow) {
            iframe.contentWindow.location.reload();
        }
    }
    get renderOnSave() {
        return this._renderOnSave;
    }
    set renderOnSave(renderOnSave) {
        this._renderOnSave = renderOnSave;
    }
}
export class ClassicRenderFactory extends ABCWidgetFactory {
    getPreviewUrl;
    defaultRenderOnSave = false;
    constructor(getPreviewUrl, options) {
        super(options);
        this.getPreviewUrl = getPreviewUrl;
    }
    createNewWidget(context) {
        return new ClassicRender({
            context,
            getPreviewUrl: this.getPreviewUrl,
            renderOnSave: this.defaultRenderOnSave
        });
    }
}
//# sourceMappingURL=classic.js.map