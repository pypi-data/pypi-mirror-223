import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import '../../../style/index.css';
declare const plugins: (JupyterFrontEndPlugin<void> | JupyterFrontEndPlugin<import("./notebook/classic/classic").INotebookRenderTracker>)[];
export default plugins;
