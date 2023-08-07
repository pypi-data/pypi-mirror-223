import { useSelector } from "react-redux";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const consoleInitialState = {
    outputs: 0,
};
/* Selectors */
export const selectConsole = () => useSelector((state) => {
    if (state.console) {
        return state.console;
    }
    return { outputs: 0 };
});
/* Actions */
import actionCreatorFactory from "typescript-fsa";
export var ConsoleActionType;
(function (ConsoleActionType) {
    ConsoleActionType["OUTPUTS"] = "console/OUTPUTS";
    ConsoleActionType["EXECUTE"] = "console/EXECUTE";
})(ConsoleActionType || (ConsoleActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const consoleActions = {
    outputs: actionCreator(ConsoleActionType.OUTPUTS),
    execute: actionCreator(ConsoleActionType.EXECUTE),
};
/* Reducers */
export const consoleReducer = reducerWithInitialState(consoleInitialState)
    .case(consoleActions.outputs, (state, success) => {
    return {
        ...state,
        outputs: success
    };
});
//# sourceMappingURL=ConsoleState.js.map