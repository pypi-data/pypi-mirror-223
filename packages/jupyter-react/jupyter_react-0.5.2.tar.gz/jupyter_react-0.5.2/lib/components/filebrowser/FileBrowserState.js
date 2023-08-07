import actionCreatorFactory from "typescript-fsa";
import { useSelector } from "react-redux";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const fileBrowserInitialState = {
    outputs: 0
};
/* Selectors */
export const selectFileBrowser = () => useSelector((state) => {
    if (state.fileBrowser) {
        return state.fileBrowser;
    }
    return { outputs: 0 };
});
/* Actions */
export var FileBrowserActionType;
(function (FileBrowserActionType) {
    FileBrowserActionType["OUTPUTS"] = "fileBrowser/OUTPUTS";
    FileBrowserActionType["EXECUTE"] = "fileBrowser/EXECUTE";
})(FileBrowserActionType || (FileBrowserActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const fileBrowserActions = {
    outputs: actionCreator(FileBrowserActionType.OUTPUTS),
    execute: actionCreator(FileBrowserActionType.EXECUTE),
};
/* Reducers */
export const fileBrowserReducer = reducerWithInitialState(fileBrowserInitialState)
    .case(fileBrowserActions.outputs, (state, success) => {
    return {
        ...state,
        outputs: success,
    };
});
//# sourceMappingURL=FileBrowserState.js.map