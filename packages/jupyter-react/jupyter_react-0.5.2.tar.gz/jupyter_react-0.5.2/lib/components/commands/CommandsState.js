import actionCreatorFactory from "typescript-fsa";
import { useSelector } from "react-redux";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const commandsInitialState = {
    outputs: 0
};
/* Selectors */
export const selectCommands = () => useSelector((state) => {
    if (state.commands) {
        return state.commands;
    }
    return { outputs: 0 };
});
/* Actions */
export var CommandsActionType;
(function (CommandsActionType) {
    CommandsActionType["OUTPUTS"] = "commands/OUTPUTS";
    CommandsActionType["EXECUTE"] = "commands/EXECUTE";
})(CommandsActionType || (CommandsActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const commandsActions = {
    outputs: actionCreator(CommandsActionType.OUTPUTS),
    execute: actionCreator(CommandsActionType.EXECUTE),
};
/* Reducers */
export const commandsReducer = reducerWithInitialState(commandsInitialState)
    .case(commandsActions.outputs, (state, success) => {
    return {
        ...state,
        outputs: success
    };
});
//# sourceMappingURL=CommandsState.js.map