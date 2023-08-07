/// <reference types="react" />
import { Store } from 'redux';
import { ICellHeader } from '@jupyterlab/cells';
import { CommandRegistry } from '@lumino/commands';
import { LuminoReactPortal } from '../../../../../jupyter/lumino/LuminoReactPortal';
export declare const DATALAYER_CELL_HEADER_CLASS = "dla-CellHeader-Container";
export type CellSidebarProps = {
    notebookId: string;
    cellId: string;
    command: CommandRegistry;
    nbgrader: boolean;
};
export declare class CellSidebarWidget extends LuminoReactPortal implements ICellHeader {
    private readonly commands;
    constructor(CellSidebar: (props: CellSidebarProps) => JSX.Element, notebookId: string, nbgrader: boolean, commands: CommandRegistry, store: Store);
}
export default CellSidebarWidget;
