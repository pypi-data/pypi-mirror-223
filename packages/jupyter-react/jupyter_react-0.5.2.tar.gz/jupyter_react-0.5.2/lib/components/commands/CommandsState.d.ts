export type ICommand = number;
export interface ICommandState {
    outputs: ICommand;
}
export declare const commandsInitialState: ICommandState;
export declare const selectCommands: () => ICommandState;
export declare enum CommandsActionType {
    OUTPUTS = "commands/OUTPUTS",
    EXECUTE = "commands/EXECUTE"
}
export declare const commandsActions: {
    outputs: import("typescript-fsa").ActionCreator<number>;
    execute: import("typescript-fsa").ActionCreator<void>;
};
export declare const commandsReducer: import("typescript-fsa-reducers").ReducerBuilder<ICommandState, ICommandState>;
