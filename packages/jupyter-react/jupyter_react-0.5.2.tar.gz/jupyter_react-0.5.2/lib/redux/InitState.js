import { useSelector } from "react-redux";
import actionCreatorFactory from "typescript-fsa";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const initInitialState = {
    start: undefined,
};
/* Selectors */
export const selectStart = () => useSelector((state) => {
    if (state.init) {
        return state.init.start;
    }
    return initInitialState.start;
});
/* Actions */
export var InitActionType;
(function (InitActionType) {
    InitActionType["GET_START"] = "jupyterReact/GET_START";
})(InitActionType || (InitActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const initActions = {
    getStart: actionCreator(InitActionType.GET_START),
};
/* Reducers */
export const initReducer = reducerWithInitialState(initInitialState)
    .case(initActions.getStart, (state, start) => {
    return {
        ...state,
        start,
    };
});
//# sourceMappingURL=InitState.js.map