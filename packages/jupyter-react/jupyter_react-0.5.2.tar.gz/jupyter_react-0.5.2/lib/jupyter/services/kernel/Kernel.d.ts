import { Kernel as JupyterKernel, KernelManager, KernelMessage } from '@jupyterlab/services';
import { ISessionConnection } from '@jupyterlab/services/lib/session/session';
export type IKernelProps = {
    kernelManager: KernelManager;
    kernelName: string;
    kernelModel?: JupyterKernel.IModel;
};
export declare class Kernel {
    private _kernelManager;
    private _kernelName;
    private _kernelConnection;
    private _session;
    private _id;
    private _info;
    constructor(props: IKernelProps);
    private requestJupyterKernel;
    get id(): string;
    get info(): KernelMessage.IInfoReply;
    get session(): ISessionConnection;
    get connection(): Promise<JupyterKernel.IKernelConnection>;
    shutdown(): void;
}
export default Kernel;
