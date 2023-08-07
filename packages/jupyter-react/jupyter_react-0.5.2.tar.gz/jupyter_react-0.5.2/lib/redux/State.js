import { combineReducers } from "redux";
import { combineEpics } from "redux-observable";
import { initInitialState, initReducer } from "./InitState";
import { cellInitialState, cellReducer } from "../components/cell/CellState";
import { notebookInitialState, notebookEpics, notebookReducer } from "../components/notebook/NotebookState";
import { terminalInitialState, terminalReducer } from "../components/terminal/TerminalState";
import { outputInitialState, outputReducer } from "../components/output/OutputState";
export const initialState = {
    init: initInitialState,
    cell: cellInitialState,
    output: outputInitialState,
    notebook: notebookInitialState,
    terminal: terminalInitialState,
};
/* Actions
export type ActionUnion<
  A extends { [asyncActionCreator: string]: (...args: any[]) => any; }
> = Exclude<ReturnType<A[keyof A]>, (...args: any[]) => Promise<void>>;

export type CellAction = ActionUnion<typeof cellActions>;
export type NotebookAction = ActionUnion<typeof notebookActions>;

export type AppAction = CellAction | NotebookAction;
*/
/* Epics */
export const epics = combineEpics(notebookEpics);
/* Reducers */
export const reducers = combineReducers({
    init: initReducer,
    cell: cellReducer,
    output: outputReducer,
    notebook: notebookReducer,
    terminal: terminalReducer,
});
//# sourceMappingURL=State.js.map