declare namespace OutputState {
    type ISource = {
        sourceId: string;
        source: string;
        increment?: number;
    };
    type IDataset = {
        sourceId: string;
        dataset: any;
        increment?: number;
    };
    type IExecute = {
        sourceId: string;
        source: string;
        increment?: number;
    };
    type IGrade = {
        sourceId: string;
        success: boolean;
        increment?: number;
    };
}
export type IOutputState = {
    source?: OutputState.ISource;
    dataset?: OutputState.IDataset;
    setSource?: OutputState.ISource;
    execute?: OutputState.IExecute;
    grade?: OutputState.IGrade;
};
export interface IOutputsState {
    outputs: Map<string, IOutputState>;
}
export declare const outputInitialState: IOutputsState;
export declare const selectJupyterSource: (id: string) => OutputState.ISource | undefined;
export declare const selectJupyterSetSource: (id: string) => OutputState.ISource | undefined;
export declare const selectDataset: (id: string) => OutputState.IDataset | undefined;
export declare const selectExecute: (id: string) => OutputState.IExecute | undefined;
export declare const selectGrade: (id: string) => OutputState.IGrade | undefined;
export declare enum OutputActionType {
    SOURCE = "output/SOURCE",
    DATASET = "output/DATASET",
    EXECUTE = "output/EXECUTE",
    SET_SOURCE = "output/SET_SOURCE",
    GRADE = "output/GRADE"
}
export declare const outputActions: {
    source: import("typescript-fsa").ActionCreator<OutputState.ISource>;
    dataset: import("typescript-fsa").ActionCreator<OutputState.IDataset>;
    execute: import("typescript-fsa").ActionCreator<OutputState.IExecute>;
    setSource: import("typescript-fsa").ActionCreator<OutputState.IExecute>;
    grade: import("typescript-fsa").ActionCreator<OutputState.IGrade>;
};
export declare const outputReducer: import("typescript-fsa-reducers").ReducerBuilder<IOutputsState, IOutputsState>;
export {};
