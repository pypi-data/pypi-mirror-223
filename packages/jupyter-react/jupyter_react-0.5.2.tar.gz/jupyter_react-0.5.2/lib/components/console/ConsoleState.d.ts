export type IConsole = number;
export interface IConsoleState {
    outputs: IConsole;
}
export declare const consoleInitialState: IConsoleState;
export declare const selectConsole: () => IConsoleState;
export declare enum ConsoleActionType {
    OUTPUTS = "console/OUTPUTS",
    EXECUTE = "console/EXECUTE"
}
export declare const consoleActions: {
    outputs: import("typescript-fsa").ActionCreator<number>;
    execute: import("typescript-fsa").ActionCreator<void>;
};
export declare const consoleReducer: import("typescript-fsa-reducers").ReducerBuilder<IConsoleState, IConsoleState>;
