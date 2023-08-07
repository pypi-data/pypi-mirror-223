import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { INotebookRenderTracker } from './classic';
export declare namespace CommandIDs {
    const classicRender = "notebook:render-with-classic";
    const classicOpen = "notebook:open-with-classic";
}
/**
 * Initialization data for the jupyterlab-preview extension.
 */
declare const notebookClassicPlugin: JupyterFrontEndPlugin<INotebookRenderTracker>;
export default notebookClassicPlugin;
