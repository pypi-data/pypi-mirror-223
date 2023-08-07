export type ISettings = number;
export interface ISettingsState {
    outputs: ISettings;
}
export declare const settingsInitialState: ISettingsState;
export declare const selectSettings: () => ISettingsState;
export declare enum SettingsActionType {
    OUTPUTS = "settings/OUTPUTS",
    EXECUTE = "settings/EXECUTE"
}
export declare const settingsActions: {
    outputs: import("typescript-fsa").ActionCreator<number>;
    execute: import("typescript-fsa").ActionCreator<void>;
};
export declare const settingsReducer: import("typescript-fsa-reducers").ReducerBuilder<ISettingsState, ISettingsState>;
