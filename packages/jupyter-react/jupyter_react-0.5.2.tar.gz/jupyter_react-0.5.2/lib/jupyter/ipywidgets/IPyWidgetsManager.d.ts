import { ManagerBase } from '@jupyter-widgets/base-manager';
export declare class IPyWidgetsManager extends ManagerBase {
    private el;
    constructor(el: any);
    loadClass(className: string, moduleName: string, moduleVersion: string): Promise<any>;
    display_view(view: any): Promise<any>;
    _get_comm_info(): Promise<{}>;
    _create_comm(): Promise<never>;
}
export default IPyWidgetsManager;
