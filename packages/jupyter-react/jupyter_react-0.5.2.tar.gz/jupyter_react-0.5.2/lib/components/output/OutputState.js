import { useSelector } from "react-redux";
import actionCreatorFactory from "typescript-fsa";
import { reducerWithInitialState } from "typescript-fsa-reducers";
export const outputInitialState = {
    outputs: new Map(),
};
/* Selectors */
export const selectJupyterSource = (id) => useSelector((state) => {
    if (state.output) {
        return state.output.outputs.get(id)?.source;
    }
    return undefined;
});
export const selectJupyterSetSource = (id) => useSelector((state) => {
    if (state.output) {
        return state.output.outputs.get(id)?.setSource;
    }
    return undefined;
});
export const selectDataset = (id) => useSelector((state) => {
    if (state.output) {
        return state.output.outputs.get(id)?.dataset;
    }
    return undefined;
});
export const selectExecute = (id) => useSelector((state) => {
    if (state.output) {
        return state.output.outputs.get(id)?.execute;
    }
    return undefined;
});
export const selectGrade = (id) => useSelector((state) => {
    if (state.output) {
        return state.output.outputs.get(id)?.grade;
    }
    return undefined;
});
/* Actions */
export var OutputActionType;
(function (OutputActionType) {
    OutputActionType["SOURCE"] = "output/SOURCE";
    OutputActionType["DATASET"] = "output/DATASET";
    OutputActionType["EXECUTE"] = "output/EXECUTE";
    OutputActionType["SET_SOURCE"] = "output/SET_SOURCE";
    OutputActionType["GRADE"] = "output/GRADE";
})(OutputActionType || (OutputActionType = {}));
const actionCreator = actionCreatorFactory('jupyterOutput');
export const outputActions = {
    source: actionCreator(OutputActionType.SOURCE),
    dataset: actionCreator(OutputActionType.DATASET),
    execute: actionCreator(OutputActionType.EXECUTE),
    setSource: actionCreator(OutputActionType.SET_SOURCE),
    grade: actionCreator(OutputActionType.GRADE),
};
/* Reducers */
export const outputReducer = reducerWithInitialState(outputInitialState)
    .case(outputActions.source, (state, source) => {
    const sourceId = source.sourceId;
    const outputs = state.outputs;
    const s = outputs.get(sourceId);
    if (s) {
        s.source = source;
    }
    else {
        outputs.set(sourceId, { source });
    }
    return {
        ...state,
        outputs,
    };
})
    .case(outputActions.dataset, (state, dataset) => {
    const sourceId = dataset.sourceId;
    const outputs = state.outputs;
    const d = outputs.get(sourceId);
    if (d) {
        d.dataset = dataset;
    }
    else {
        outputs.set(sourceId, { dataset });
    }
    return {
        ...state,
        outputs,
    };
})
    .case(outputActions.execute, (state, execute) => {
    const sourceId = execute.sourceId;
    const outputs = state.outputs;
    const e = outputs.get(sourceId);
    if (e) {
        e.execute = execute;
    }
    else {
        outputs.set(sourceId, { execute });
    }
    return {
        ...state,
        outputs,
    };
})
    .case(outputActions.setSource, (state, setSource) => {
    const sourceId = setSource.sourceId;
    const outputs = state.outputs;
    const s = outputs.get(sourceId);
    if (s) {
        s.setSource = setSource;
    }
    else {
        outputs.set(sourceId, { setSource });
    }
    return {
        ...state,
        outputs,
    };
})
    .case(outputActions.grade, (state, grade) => {
    const sourceId = grade.sourceId;
    const outputs = state.outputs;
    const g = outputs.get(sourceId);
    if (g) {
        g.grade = grade;
    }
    else {
        outputs.set(sourceId, { grade });
    }
    return {
        ...state,
        outputs,
    };
});
//# sourceMappingURL=OutputState.js.map