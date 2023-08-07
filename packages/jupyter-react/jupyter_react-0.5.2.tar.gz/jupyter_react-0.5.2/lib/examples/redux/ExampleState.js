import { useSelector } from "react-redux";
import actionCreatorFactory from "typescript-fsa";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const initExampleState = {
    foo: undefined,
};
/* Selectors */
export const selectFoo = () => useSelector((state) => {
    if (state.init) {
        return state.init.foo;
    }
    return initExampleState.foo;
});
/* Actions */
export var ExampleActionType;
(function (ExampleActionType) {
    ExampleActionType["UPDATE_FOO"] = "jupyterReact/UPDATE_FOO";
})(ExampleActionType || (ExampleActionType = {}));
const actionCreator = actionCreatorFactory('jupyterReact');
export const exampleActions = {
    updateFoo: actionCreator(ExampleActionType.UPDATE_FOO),
};
/* Reducers */
export const exampleReducer = reducerWithInitialState(initExampleState)
    .case(exampleActions.updateFoo, (state, foo) => {
    return {
        ...state,
        foo,
    };
});
//# sourceMappingURL=ExampleState.js.map