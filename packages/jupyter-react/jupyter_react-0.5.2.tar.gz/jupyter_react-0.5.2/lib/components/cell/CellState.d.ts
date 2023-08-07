import CellAdapter from "./CellAdapter";
export interface ICellState {
    source: string;
    outputsCount: number;
    kernelAvailable: boolean;
    adapter?: CellAdapter;
}
export declare const cellInitialState: ICellState;
export declare const selectCell: () => ICellState;
export declare enum CellActionType {
    SOURCE = "cell/SOURCE",
    OUTPUTS_COUNT = "cell/OUTPUTS_COUNT",
    EXECUTE = "cell/EXECUTE",
    UPDATE = "cell/UPDATE"
}
export declare const cellActions: {
    source: import("typescript-fsa").ActionCreator<string>;
    outputsCount: import("typescript-fsa").ActionCreator<number>;
    execute: import("typescript-fsa").ActionCreator<void>;
    update: import("typescript-fsa").ActionCreator<Partial<ICellState>>;
};
export declare const cellReducer: import("typescript-fsa-reducers").ReducerBuilder<ICellState, ICellState>;
