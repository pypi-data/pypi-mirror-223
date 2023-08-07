import actionCreatorFactory from "typescript-fsa";
import { useSelector } from "react-redux";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const cellInitialState = {
    source: '',
    outputsCount: -1,
    kernelAvailable: false,
};
/* Selectors */
export const selectCell = () => useSelector((state) => {
    if (state.cell) {
        return state.cell;
    }
    return cellInitialState;
});
/* Actions */
export var CellActionType;
(function (CellActionType) {
    CellActionType["SOURCE"] = "cell/SOURCE";
    CellActionType["OUTPUTS_COUNT"] = "cell/OUTPUTS_COUNT";
    CellActionType["EXECUTE"] = "cell/EXECUTE";
    CellActionType["UPDATE"] = "cell/UPDATE";
})(CellActionType || (CellActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const cellActions = {
    source: actionCreator(CellActionType.SOURCE),
    outputsCount: actionCreator(CellActionType.OUTPUTS_COUNT),
    execute: actionCreator(CellActionType.EXECUTE),
    update: actionCreator(CellActionType.UPDATE),
};
/* Reducers */
export const cellReducer = reducerWithInitialState(cellInitialState)
    .case(cellActions.execute, (state, payload) => {
    if (state.adapter) {
        state.adapter.execute();
    }
    return {
        ...state,
    };
})
    .case(cellActions.source, (state, source) => {
    return {
        ...state,
        source,
    };
})
    .case(cellActions.update, (state, partial) => ({
    ...state,
    ...partial,
}))
    .case(cellActions.outputsCount, (state, outputsCount) => {
    return {
        ...state,
        outputsCount,
    };
});
//# sourceMappingURL=CellState.js.map