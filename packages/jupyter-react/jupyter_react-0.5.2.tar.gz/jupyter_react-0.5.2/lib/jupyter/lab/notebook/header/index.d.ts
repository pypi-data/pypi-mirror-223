import { IDisposable } from '@lumino/disposable';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';
export declare class NotebookHeaderExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
    createNew(panel: NotebookPanel, _: DocumentRegistry.IContext<INotebookModel>): IDisposable;
}
