import { INotebookContent } from '@jupyterlab/nbformat';
import { INotebookModel, NotebookModelFactory } from "@jupyterlab/notebook";
import { DocumentRegistry } from '@jupyterlab/docregistry';
import type { ISharedNotebook } from '@jupyter/ydoc';
export declare class JupyterReactNotebookModelFactory extends NotebookModelFactory {
    private _nbformat?;
    /** @override */
    constructor(options: DatalayerNotebookModelFactory.IOptions);
    /** @override */
    createNew(options: DocumentRegistry.IModelOptions<ISharedNotebook>): INotebookModel;
}
export declare namespace DatalayerNotebookModelFactory {
    interface IOptions extends NotebookModelFactory.IOptions {
        nbformat?: INotebookContent;
    }
}
export default JupyterReactNotebookModelFactory;
