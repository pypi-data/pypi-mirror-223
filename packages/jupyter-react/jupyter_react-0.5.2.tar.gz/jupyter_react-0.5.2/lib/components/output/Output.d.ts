import { IOutput } from '@jupyterlab/nbformat';
import OutputAdapter from './OutputAdapter';
import Kernel from '../../jupyter/services/kernel/Kernel';
import './Output.css';
export type IOutputProps = {
    outputs?: IOutput[];
    adapter?: OutputAdapter;
    kernel: Kernel;
    autoRun: boolean;
    disableRun: boolean;
    showEditor: boolean;
    code: string;
    codePre?: string;
    clearTrigger: number;
    sourceId: string;
    receipt?: string;
    executeTrigger: number;
    toolbarPosition: 'up' | 'middle' | 'none';
    insertText?: (payload?: any) => string;
    luminoWidgets: boolean;
};
export declare const Output: {
    (props: IOutputProps): import("react/jsx-runtime").JSX.Element;
    defaultProps: Partial<IOutputProps>;
};
export default Output;
