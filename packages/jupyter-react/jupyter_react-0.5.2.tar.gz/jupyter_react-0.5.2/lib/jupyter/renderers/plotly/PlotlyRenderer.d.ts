import { Widget } from "@lumino/widgets";
import { Message } from "@lumino/messaging";
import { IRenderMime } from "@jupyterlab/rendermime-interfaces";
import "./plotly.css";
/**
 * The MIME type for Plotly.
 * The version of this follows the major version of Plotly.
 */
export declare const MIME_TYPE = "application/vnd.plotly.v1+json";
export declare class RenderedPlotly extends Widget implements IRenderMime.IRenderer {
    /**
     * Create a new widget for rendering Plotly.
     */
    constructor(options: IRenderMime.IRendererOptions);
    /**
     * Render Plotly into this widget's node.
     */
    renderModel(model: IRenderMime.IMimeModel): Promise<void>;
    private hasGraphElement;
    private updateImage;
    private hideGraph;
    private showGraph;
    private hideImage;
    private showImage;
    private createGraph;
    /**
     * A message handler invoked on an `'after-show'` message.
     */
    protected onAfterShow(msg: Message): void;
    /**
     * A message handler invoked on a `'resize'` message.
     */
    protected onResize(msg: Widget.ResizeMessage): void;
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    protected onUpdateRequest(msg: Message): void;
    private _mimeType;
    private _img_el;
    private _model;
    private static Plotly;
    private static _resolveLoadingPlotly;
    private static loadingPlotly;
}
/**
 * A mime renderer factory for Plotly data.
 */
export declare const rendererFactory: IRenderMime.IRendererFactory;
declare const extensions: IRenderMime.IExtension | IRenderMime.IExtension[];
export default extensions;
