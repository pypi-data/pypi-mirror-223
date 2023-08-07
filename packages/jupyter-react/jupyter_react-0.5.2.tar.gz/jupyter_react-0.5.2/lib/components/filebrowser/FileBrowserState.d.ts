export type IFileBrowser = number;
export interface IFileBrowserState {
    outputs: IFileBrowser;
}
export declare const fileBrowserInitialState: IFileBrowserState;
export declare const selectFileBrowser: () => IFileBrowserState;
export declare enum FileBrowserActionType {
    OUTPUTS = "fileBrowser/OUTPUTS",
    EXECUTE = "fileBrowser/EXECUTE"
}
export declare const fileBrowserActions: {
    outputs: import("typescript-fsa").ActionCreator<number>;
    execute: import("typescript-fsa").ActionCreator<void>;
};
export declare const fileBrowserReducer: import("typescript-fsa-reducers").ReducerBuilder<IFileBrowserState, IFileBrowserState>;
