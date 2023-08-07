export interface IInitState {
    start?: Date;
}
export declare const initInitialState: IInitState;
export declare const selectStart: () => Date | undefined;
export declare enum InitActionType {
    GET_START = "jupyterReact/GET_START"
}
export declare const initActions: {
    getStart: import("typescript-fsa").ActionCreator<Date>;
};
export declare const initReducer: import("typescript-fsa-reducers").ReducerBuilder<IInitState, IInitState>;
