import { ISessionContext } from '@jupyterlab/apputils';
import { IOutput } from '@jupyterlab/nbformat';
import { Kernel, KernelMessage } from '@jupyterlab/services';
import { ISignal } from '@lumino/signaling';
export declare class KernelModel {
    constructor(session: ISessionContext);
    get future(): Kernel.IFuture<KernelMessage.IExecuteRequestMsg, KernelMessage.IExecuteReplyMsg> | null;
    set future(value: Kernel.IFuture<KernelMessage.IExecuteRequestMsg, KernelMessage.IExecuteReplyMsg> | null);
    get output(): IOutput | null;
    get stateChanged(): ISignal<KernelModel, void>;
    execute(code: string): void;
    private _onIOPub;
    private _future;
    private _output;
    private _sessionContext;
    private _stateChanged;
}
export default KernelModel;
