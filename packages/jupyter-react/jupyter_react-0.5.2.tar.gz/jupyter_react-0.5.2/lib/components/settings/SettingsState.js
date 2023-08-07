import { useSelector } from "react-redux";
import actionCreatorFactory from "typescript-fsa";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const settingsInitialState = {
    outputs: 0,
};
/* Selectors */
export const selectSettings = () => useSelector((state) => {
    if (state.settings) {
        return state.settings;
    }
    return { outputs: 0 };
});
/* Actions */
export var SettingsActionType;
(function (SettingsActionType) {
    SettingsActionType["OUTPUTS"] = "settings/OUTPUTS";
    SettingsActionType["EXECUTE"] = "settings/EXECUTE";
})(SettingsActionType || (SettingsActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const settingsActions = {
    outputs: actionCreator(SettingsActionType.OUTPUTS),
    execute: actionCreator(SettingsActionType.EXECUTE),
};
/* Reducers */
export const settingsReducer = reducerWithInitialState(settingsInitialState)
    .case(settingsActions.outputs, (state, success) => {
    return {
        ...state,
        outputs: success
    };
});
//# sourceMappingURL=SettingsState.js.map