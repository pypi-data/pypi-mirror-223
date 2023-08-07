import { IOutput } from '@jupyterlab/nbformat';
import { OutputArea } from '@jupyterlab/outputarea';
import Kernel from "./../../jupyter/services/kernel/Kernel";
export declare class OutputAdapter {
    private _kernel?;
    private _renderers;
    private _outputArea;
    private _rendermime;
    private _iPyWidgetsClassicManager;
    constructor(kernel: Kernel | undefined, outputs?: IOutput[]);
    execute(code: string): void;
    interrupt(): void;
    clearOutput(): void;
    get kernel(): Kernel | undefined;
    set kernel(kernel: Kernel | undefined);
    get outputArea(): OutputArea;
    private initKernel;
}
export default OutputAdapter;
