import { ServiceManager } from '@jupyterlab/services';
export declare class Services {
    private _serviceManager;
    constructor(services: ServiceManager);
    kernelspecs(): import("@jupyterlab/services/lib/kernelspec/kernelspec").IManager;
    contents(): import("@jupyterlab/services").Contents.IManager;
    nbconvert(): import("@jupyterlab/services").NbConvert.IManager;
    sessions(): import("@jupyterlab/services/lib/session/session").IManager;
    settings(): import("@jupyterlab/services").Setting.IManager;
    terminals(): import("@jupyterlab/services/lib/terminal/terminal").IManager;
    workspaces(): import("@jupyterlab/services").Workspace.IManager;
    builder(): import("@jupyterlab/services").Builder.IManager;
    serverSettings(): import("@jupyterlab/services").ServerConnection.ISettings;
    refreshKernelspecs(): Promise<void>;
    getKernelspecs(): import("@jupyterlab/services/lib/kernelspec/restapi").ISpecModels | null;
}
export default Services;
