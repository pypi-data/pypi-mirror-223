import { Kernel } from '@jupyterlab/services';
import { WidgetModel, WidgetView, DOMWidgetView, ICallbacks } from '@jupyter-widgets/base';
import { HTMLManager } from "@jupyter-widgets/html-manager";
/**
 * The class responsible for the classic IPyWidget rendering.
 */
export declare class IPyWidgetsClassicManager extends HTMLManager {
    _kernelConnection: Kernel.IKernelConnection | null;
    private _commRegistration;
    private _onError;
    registerWithKernel(kernelConnection: Kernel.IKernelConnection | null): void;
    get onError(): any;
    display_view(view: Promise<DOMWidgetView> | DOMWidgetView, el: HTMLElement): Promise<void>;
    loadClass(className: string, moduleName: any, moduleVersion: string): Promise<typeof WidgetModel | typeof WidgetView>;
    callbacks(view: WidgetView): ICallbacks;
    _create_comm(target_name: any, model_id: string, data?: any, metadata?: any, buffers?: ArrayBuffer[] | ArrayBufferView[]): Promise<any>;
    _get_comm_info(): Promise<{}>;
}
