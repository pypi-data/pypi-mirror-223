export interface IExampleState {
    foo?: Date;
}
export declare const initExampleState: IExampleState;
export declare const selectFoo: () => Date | undefined;
export declare enum ExampleActionType {
    UPDATE_FOO = "jupyterReact/UPDATE_FOO"
}
export declare const exampleActions: {
    updateFoo: import("typescript-fsa").ActionCreator<Date>;
};
export declare const exampleReducer: import("typescript-fsa-reducers").ReducerBuilder<IExampleState, IExampleState>;
