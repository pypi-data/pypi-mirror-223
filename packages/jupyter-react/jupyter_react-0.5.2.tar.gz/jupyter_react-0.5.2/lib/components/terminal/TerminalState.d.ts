import TerminalAdapter from "./TerminalAdapter";
export type ITerminal = boolean;
export interface ITerminalState {
    dark: ITerminal;
    adapter?: TerminalAdapter;
}
export declare const terminalInitialState: ITerminalState;
export declare const selectTerminal: () => ITerminalState;
export declare enum TerminalActionType {
    UPDATE = "terminal/UPDATE"
}
export declare const terminalActions: {
    update: import("typescript-fsa").ActionCreator<Partial<ITerminalState>>;
};
export declare const terminalReducer: import("typescript-fsa-reducers").ReducerBuilder<ITerminalState, ITerminalState>;
