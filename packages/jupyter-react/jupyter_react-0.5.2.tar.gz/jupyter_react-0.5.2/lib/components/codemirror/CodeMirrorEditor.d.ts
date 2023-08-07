import Kernel from './../../jupyter/services/kernel/Kernel';
import OutputAdapter from '../output/OutputAdapter';
export declare const CodeMirrorEditor: (props: {
    code: string;
    codePre?: string | undefined;
    outputAdapter: OutputAdapter;
    kernel?: Kernel | undefined;
    autoRun: boolean;
    disableRun: boolean;
    sourceId: string;
    toolbarPosition: 'up' | 'middle' | 'none';
    insertText?: ((payload?: any) => string) | undefined;
}) => import("react/jsx-runtime").JSX.Element;
export default CodeMirrorEditor;
