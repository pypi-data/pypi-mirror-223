import { useSelector } from "react-redux";
import actionCreatorFactory from "typescript-fsa";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const terminalInitialState = {
    dark: false,
};
/* Selectors */
export const selectTerminal = () => useSelector((state) => {
    if (state.terminal) {
        return state.terminal;
    }
    return terminalInitialState;
});
/* Actions */
export var TerminalActionType;
(function (TerminalActionType) {
    TerminalActionType["UPDATE"] = "terminal/UPDATE";
})(TerminalActionType || (TerminalActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const terminalActions = {
    update: actionCreator(TerminalActionType.UPDATE),
};
/* Reducers */
export const terminalReducer = reducerWithInitialState(terminalInitialState)
    .case(terminalActions.update, (state, update) => {
    if (state.adapter) {
        if (update.dark !== undefined) {
            if (update.dark) {
                state.adapter.setTheme('dark');
            }
            else {
                state.adapter.setTheme('light');
            }
        }
    }
    return {
        ...state,
        ...update,
    };
});
//# sourceMappingURL=TerminalState.js.map