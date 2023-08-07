import { ReactPortal } from "react";
import * as nbformat from "@jupyterlab/nbformat";
import { INotebookModel } from "@jupyterlab/notebook";
import { NotebookChange } from "@jupyter/ydoc";
import { Cell, ICellModel } from "@jupyterlab/cells";
import { Kernel as JupyterKernel } from "@jupyterlab/services";
import Kernel from "./../../jupyter/services/kernel/Kernel";
import NotebookAdapter from "./NotebookAdapter";
type PortalDisplay = {
    portal: ReactPortal;
    pinned: boolean;
};
export type INotebookState = {
    model?: INotebookModel;
    adapter?: NotebookAdapter;
    saveRequest?: Date;
    activeCell?: Cell<ICellModel>;
    kernelStatus?: JupyterKernel.Status;
    notebookChange?: NotebookChange;
    portals: ReactPortal[];
    portalDisplay?: PortalDisplay;
};
export interface INotebooksState {
    notebooks: Map<string, INotebookState>;
}
export declare const notebookInitialState: INotebooksState;
export declare const selectNotebook: (uid: string) => INotebookState | undefined;
export declare const selectNotebookModel: (uid: string) => {
    model: INotebookModel | undefined;
    changed: any;
} | undefined;
export declare const selectKernelStatus: (uid: string) => string | undefined;
export declare const selectActiveCell: (uid: string) => Cell<ICellModel> | undefined;
export declare const selectNotebookPortals: (uid: string) => ReactPortal[] | undefined;
export declare const selectSaveRequest: (uid: string) => Date | undefined;
export declare const selectNotebookPortalDisplay: (uid: string) => PortalDisplay | undefined;
export declare enum ActionType {
    ACTIVE_CELL_CHANGE = "notebook/ACTIVE_CELL_CHANGE",
    ADD_PORTALS = "notebook/ADD_PORTALS",
    CHANGE_CELL_TYPE = "notebook/CHANGE_CELL_TYPE",
    CHANGE_KERNEL = "notebook/CHANGE_KERNEL",
    DELETE = "notebook/DELETE",
    DISPOSE = "notebook/DISPOSE",
    INSERT_ABOVE = "notebook/INSERT_ABOVE",
    INSERT_BELOW = "notebook/INSERT_BELOW",
    INTERRUPT = "notebook/INTERRUPT",
    KERNEL_STATUS_CHANGE = "notebook/KERNEL_STATUS_CHANGE",
    MODEL_CHANGE = "notebook/MODEL_CHANGE",
    NOTEBOOK_CHANGE = "notebook/NOTEBOOK_CHANGE",
    RESET = "notebook/RESET",
    RUN = "notebook/RUN",
    RUN_ALL = "notebook/RUN_ALL",
    SAVE = "notebook/SAVE",
    SET_PORTALS = "notebook/SET_PORTALS",
    SET_PORTAL_DISPLAY = "notebook/SET_PORTAL_DISPLAY",
    UPDATE = "notebook/UPDATE"
}
type UpdateUid = {
    uid: string;
    partialState: Partial<INotebookState>;
};
type NotebookChangeUid = {
    uid: string;
    notebookChange: NotebookChange;
};
type NotebookModelUid = {
    uid: string;
    notebookModel: INotebookModel;
};
type CellModelUid = {
    uid: string;
    cellModel?: Cell<ICellModel>;
};
type KernelStatusUid = {
    uid: string;
    kernelStatus: JupyterKernel.Status;
};
type KernelChangeUid = {
    uid: string;
    kernel: Kernel;
};
type ReactPortalsUid = {
    uid: string;
    portals: ReactPortal[];
};
type PortalDisplayUid = {
    uid: string;
    portalDisplay: PortalDisplay | undefined;
};
type DateUid = {
    uid: string;
    date: Date | undefined;
};
type CellTypeUid = {
    uid: string;
    cellType: nbformat.CellType;
};
export declare const notebookActions: {
    reset: import("typescript-fsa").ActionCreator<string>;
    update: import("typescript-fsa").ActionCreator<UpdateUid>;
    notebookChange: import("typescript-fsa").ActionCreator<NotebookChangeUid>;
    modelChange: import("typescript-fsa").ActionCreator<NotebookModelUid>;
    changeKernel: import("typescript-fsa").ActionCreator<KernelChangeUid>;
    activeCellChange: import("typescript-fsa").ActionCreator<CellModelUid>;
    kernelStatusChanged: import("typescript-fsa").ActionCreator<KernelStatusUid>;
    addPortals: import("typescript-fsa").ActionCreator<ReactPortalsUid>;
    setPortals: import("typescript-fsa").ActionCreator<ReactPortalsUid>;
    setPortalDisplay: import("typescript-fsa").ActionCreator<PortalDisplayUid>;
    dispose: import("typescript-fsa").ActionCreator<string>;
    save: import("typescript-fsa").AsyncActionCreators<DateUid, DateUid, {}>;
    run: import("typescript-fsa").AsyncActionCreators<string, string, {}>;
    runAll: import("typescript-fsa").AsyncActionCreators<string, string, {}>;
    interrupt: import("typescript-fsa").AsyncActionCreators<string, string, {}>;
    insertAbove: import("typescript-fsa").AsyncActionCreators<CellTypeUid, CellTypeUid, {}>;
    insertBelow: import("typescript-fsa").AsyncActionCreators<CellTypeUid, CellTypeUid, {}>;
    delete: import("typescript-fsa").AsyncActionCreators<string, string, {}>;
    changeCellType: import("typescript-fsa").AsyncActionCreators<CellTypeUid, CellTypeUid, {}>;
};
export declare const notebookEpics: any;
export declare const notebookReducer: import("typescript-fsa-reducers").ReducerBuilder<INotebooksState, INotebooksState>;
export {};
