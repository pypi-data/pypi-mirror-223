import { EditorView } from 'codemirror';
import OutputAdapter from '../output/OutputAdapter';
import Kernel from '../../jupyter/services/kernel/Kernel';
type Props = {
    editorView?: EditorView;
    codePre?: string;
    kernel: Kernel;
    outputAdapter: OutputAdapter;
    executeCode: (editorView?: EditorView, code?: string) => void;
};
export declare const CodeMirrorOutputToolbar: (props: Props) => import("react/jsx-runtime").JSX.Element;
export default CodeMirrorOutputToolbar;
