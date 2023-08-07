import { IMarkdownParser } from '@jupyterlab/rendermime';
import { IEditorLanguageRegistry } from '@jupyterlab/codemirror';
export declare const getMarked: (languages: IEditorLanguageRegistry) => IMarkdownParser;
export default getMarked;
