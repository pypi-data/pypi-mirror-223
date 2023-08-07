/// <reference types="react" />
import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { INotebookContent } from '@jupyterlab/nbformat';
import { Kernel } from "./../../jupyter/services/kernel/Kernel";
import { CellSidebarProps } from './cell/sidebar/lumino/CellSidebarWidget';
import './Notebook.css';
export type INotebookProps = {
    uid: string;
    path: string;
    nbformat: INotebookContent;
    kernel?: Kernel;
    readOnly: boolean;
    nbgrader: boolean;
    ipywidgets: 'classic' | 'lab';
    cellMetadataPanel: boolean;
    CellSidebar?: (props: CellSidebarProps) => JSX.Element;
    cellSidebarMargin: number;
    Toolbar?: (props: any) => JSX.Element;
    height?: string;
    maxHeight?: string;
    renderers: IRenderMime.IRendererFactory[];
};
/**
 * This component creates a Notebook as a collection of snippets
 * with sidebars.
 *
 * @param props The notebook properties.
 * @returns A Notebook React.js component.
 */
export declare const Notebook: {
    (props: INotebookProps): import("react/jsx-runtime").JSX.Element;
    defaultProps: Partial<INotebookProps>;
};
export default Notebook;
