import { IFrame, IWidgetTracker } from '@jupyterlab/apputils';
import { ABCWidgetFactory, DocumentRegistry, DocumentWidget } from '@jupyterlab/docregistry';
import { INotebookModel } from '@jupyterlab/notebook';
import { Token } from '@lumino/coreutils';
export type INotebookRenderTracker = IWidgetTracker<ClassicRender>;
export declare const INotebookRenderTracker: Token<INotebookRenderTracker>;
export declare const CLASSIC_RENDER_ICON_CLASS = "jp-MaterialIcon jp-NotebookIcon";
export declare class ClassicRender extends DocumentWidget<IFrame, INotebookModel> {
    private _renderOnSave;
    constructor(options: ClassicRender.IOptions);
    dispose(): void;
    reload(): void;
    get renderOnSave(): boolean;
    set renderOnSave(renderOnSave: boolean);
}
export declare namespace ClassicRender {
    interface IOptions extends DocumentWidget.IOptionsOptionalContent<IFrame, INotebookModel> {
        getPreviewUrl: (path: string) => string;
        renderOnSave?: boolean;
    }
}
export declare class ClassicRenderFactory extends ABCWidgetFactory<ClassicRender, INotebookModel> {
    private getPreviewUrl;
    defaultRenderOnSave: boolean;
    constructor(getPreviewUrl: (path: string) => string, options: DocumentRegistry.IWidgetFactoryOptions<ClassicRender>);
    protected createNewWidget(context: DocumentRegistry.IContext<INotebookModel>): ClassicRender;
}
