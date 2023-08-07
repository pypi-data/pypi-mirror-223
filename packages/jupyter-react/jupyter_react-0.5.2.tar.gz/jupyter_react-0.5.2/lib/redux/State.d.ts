import { AnyAction } from "typescript-fsa";
import { ICellState } from "../components/cell/CellState";
import { INotebooksState } from "../components/notebook/NotebookState";
import { ITerminalState } from "../components/terminal/TerminalState";
import { IOutputsState } from "../components/output/OutputState";
export interface IJupyterReactState {
    init: any;
    cell: ICellState;
    output: IOutputsState;
    notebook: INotebooksState;
    terminal: ITerminalState;
}
export declare const initialState: IJupyterReactState;
export declare const epics: import("redux-observable").Epic<AnyAction, AnyAction, any, any>;
export declare const reducers: import("redux").Reducer<import("redux").CombinedState<IJupyterReactState>, import("redux").AnyAction>;
