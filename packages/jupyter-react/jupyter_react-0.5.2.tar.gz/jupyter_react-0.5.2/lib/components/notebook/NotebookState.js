import { useSelector } from "react-redux";
import actionCreatorFactory from "typescript-fsa";
import { combineEpics } from "redux-observable";
import { reducerWithInitialState } from "typescript-fsa-reducers";
import { ignoreElements, map, tap } from "rxjs/operators";
import { ofAction } from "@datalayer/typescript-fsa-redux-observable";
import { cmdIds } from "./NotebookCommands";
export const notebookInitialState = {
    notebooks: new Map(),
};
/* Selectors */
export const selectNotebook = (uid) => useSelector((state) => {
    if (state.notebook) {
        return state.notebook.notebooks.get(uid);
    }
    return undefined;
});
export const selectNotebookModel = (uid) => useSelector((state) => {
    if (state.notebook) {
        // We need a changed attribute to deal the React-Redux shallow equality.
        return {
            model: state.notebook.notebooks.get(uid)?.model,
            changed: state.notebook.notebooks.get(uid)?.model?.contentChanged,
        };
    }
    return undefined;
});
export const selectKernelStatus = (uid) => useSelector((state) => {
    if (state.notebook) {
        return state.notebook.notebooks.get(uid)?.kernelStatus;
    }
    return undefined;
});
export const selectActiveCell = (uid) => useSelector((state) => {
    if (state.notebook) {
        return state.notebook.notebooks.get(uid)?.activeCell;
    }
    return undefined;
});
export const selectNotebookPortals = (uid) => useSelector((state) => {
    if (state.notebook) {
        return state.notebook.notebooks.get(uid)?.portals;
    }
    return undefined;
});
export const selectSaveRequest = (uid) => useSelector((state) => {
    if (state.notebook) {
        return state.notebook.notebooks.get(uid)?.saveRequest;
    }
    return undefined;
});
export const selectNotebookPortalDisplay = (uid) => useSelector((state) => {
    if (state.notebook) {
        return state.notebook.notebooks.get(uid)?.portalDisplay;
    }
    return undefined;
});
/* Actions */
export var ActionType;
(function (ActionType) {
    ActionType["ACTIVE_CELL_CHANGE"] = "notebook/ACTIVE_CELL_CHANGE";
    ActionType["ADD_PORTALS"] = "notebook/ADD_PORTALS";
    ActionType["CHANGE_CELL_TYPE"] = "notebook/CHANGE_CELL_TYPE";
    ActionType["CHANGE_KERNEL"] = "notebook/CHANGE_KERNEL";
    ActionType["DELETE"] = "notebook/DELETE";
    ActionType["DISPOSE"] = "notebook/DISPOSE";
    ActionType["INSERT_ABOVE"] = "notebook/INSERT_ABOVE";
    ActionType["INSERT_BELOW"] = "notebook/INSERT_BELOW";
    ActionType["INTERRUPT"] = "notebook/INTERRUPT";
    ActionType["KERNEL_STATUS_CHANGE"] = "notebook/KERNEL_STATUS_CHANGE";
    ActionType["MODEL_CHANGE"] = "notebook/MODEL_CHANGE";
    ActionType["NOTEBOOK_CHANGE"] = "notebook/NOTEBOOK_CHANGE";
    ActionType["RESET"] = "notebook/RESET";
    ActionType["RUN"] = "notebook/RUN";
    ActionType["RUN_ALL"] = "notebook/RUN_ALL";
    ActionType["SAVE"] = "notebook/SAVE";
    ActionType["SET_PORTALS"] = "notebook/SET_PORTALS";
    ActionType["SET_PORTAL_DISPLAY"] = "notebook/SET_PORTAL_DISPLAY";
    ActionType["UPDATE"] = "notebook/UPDATE";
})(ActionType || (ActionType = {}));
const actionCreator = actionCreatorFactory('jupyterNotebook');
export const notebookActions = {
    reset: actionCreator(ActionType.RESET),
    update: actionCreator(ActionType.UPDATE),
    notebookChange: actionCreator(ActionType.NOTEBOOK_CHANGE),
    modelChange: actionCreator(ActionType.MODEL_CHANGE),
    changeKernel: actionCreator(ActionType.CHANGE_KERNEL),
    activeCellChange: actionCreator(ActionType.ACTIVE_CELL_CHANGE),
    kernelStatusChanged: actionCreator(ActionType.KERNEL_STATUS_CHANGE),
    addPortals: actionCreator(ActionType.ADD_PORTALS),
    setPortals: actionCreator(ActionType.SET_PORTALS),
    setPortalDisplay: actionCreator(ActionType.SET_PORTAL_DISPLAY),
    dispose: actionCreator(ActionType.DISPOSE),
    save: actionCreator.async(ActionType.SAVE),
    run: actionCreator.async(ActionType.RUN),
    runAll: actionCreator.async(ActionType.RUN_ALL),
    interrupt: actionCreator.async(ActionType.INTERRUPT),
    insertAbove: actionCreator.async(ActionType.INSERT_ABOVE),
    insertBelow: actionCreator.async(ActionType.INSERT_BELOW),
    delete: actionCreator.async(ActionType.DELETE),
    changeCellType: actionCreator.async(ActionType.CHANGE_CELL_TYPE)
};
/* Epics */
const runEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.run.started), tap(action => {
    state$.value.notebook.notebooks.get(action.payload)?.adapter?.commands.execute(cmdIds.run);
}), ignoreElements());
const runAllEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.runAll.started), tap(action => {
    state$.value.notebook.notebooks.get(action.payload)?.adapter?.commands.execute(cmdIds.runAll);
}), ignoreElements());
const interruptEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.interrupt.started), tap(action => {
    state$.value.notebook.notebooks.get(action.payload)?.adapter?.commands.execute(cmdIds.interrupt);
}), ignoreElements());
const insertAboveEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.insertAbove.started), tap(action => {
    state$.value.notebook.notebooks.get(action.payload.uid)?.adapter?.setDefaultCellType(action.payload.cellType);
    state$.value.notebook.notebooks.get(action.payload.uid)?.adapter?.commands.execute(cmdIds.insertAbove);
}), ignoreElements());
const insertBelowEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.insertBelow.started), tap(action => {
    state$.value.notebook.notebooks.get(action.payload.uid)?.adapter?.setDefaultCellType(action.payload.cellType);
    state$.value.notebook.notebooks.get(action.payload.uid)?.adapter?.commands.execute(cmdIds.insertBelow);
}), ignoreElements());
const deleteEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.delete.started), tap(action => {
    state$.value.notebook.notebooks.get(action.payload)?.adapter?.commands.execute(cmdIds.deleteCells);
}), ignoreElements());
const changeCellTypeEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.changeCellType.started), tap(action => {
    //      state$.value.notebook?.adapter?.commands.execute(cmdIds.toCode);
    state$.value.notebook.notebooks.get(action.payload.uid)?.adapter?.changeCellType(action.payload.cellType);
    /*
    NotebookActions.changeCellType(
      state$.value.notebook.notebooks.get(action.payload)?.adapter?.notebookPanel?.content!,
      action.payload
    );
    */
}), ignoreElements());
const saveEpic = (action$, state$) => action$.pipe(ofAction(notebookActions.save.started), map(action => {
    state$.value.notebook.notebooks.get(action.payload.uid)?.adapter?.commands.execute(cmdIds.save);
    return notebookActions.save.done({
        params: action.payload,
        result: action.payload,
    });
}));
export const notebookEpics = combineEpics(runEpic, runAllEpic, interruptEpic, insertAboveEpic, insertBelowEpic, deleteEpic, changeCellTypeEpic, saveEpic);
/* Reducers */
export const notebookReducer = reducerWithInitialState(notebookInitialState)
    .case(notebookActions.reset, (state, _) => {
    return notebookInitialState;
})
    .case(notebookActions.update, (state, updateUid) => {
    const notebooks = state.notebooks;
    let notebook = notebooks.get(updateUid.uid);
    if (notebook) {
        notebook = { ...notebook, ...updateUid.partialState };
    }
    else {
        notebooks.set(updateUid.uid, {
            adapter: updateUid.partialState.adapter,
            portals: [],
        });
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.activeCellChange, (state, cellModelUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(cellModelUid.uid);
    if (notebook) {
        notebook.activeCell = cellModelUid.cellModel;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.modelChange, (state, notebookModelUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(notebookModelUid.uid);
    if (notebook) {
        notebook.model = notebookModelUid.notebookModel;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.notebookChange, (state, notebookChangeUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(notebookChangeUid.uid);
    if (notebook) {
        notebook.notebookChange = notebookChangeUid.notebookChange;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.kernelStatusChanged, (state, kernelStatusUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(kernelStatusUid.uid);
    if (notebook) {
        notebook.kernelStatus = kernelStatusUid.kernelStatus;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.changeKernel, (state, kernelChange) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(kernelChange.uid);
    if (notebook) {
        notebook.adapter?.changeKernel(kernelChange.kernel);
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.addPortals, (state, portalsUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(portalsUid.uid);
    if (notebook) {
        notebook.portals = notebook.portals.concat(portalsUid.portals);
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.dispose, (state, uid) => {
    const notebooks = state.notebooks;
    notebooks.delete(uid);
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.setPortals, (state, portalsUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(portalsUid.uid);
    if (notebook) {
        notebook.portals = portalsUid.portals;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.setPortalDisplay, (state, portalDisplayUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(portalDisplayUid.uid);
    if (notebook) {
        notebook.portalDisplay = portalDisplayUid.portalDisplay;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.save.done, (state, dateUid) => {
    const notebooks = state.notebooks;
    const notebook = notebooks.get(dateUid.result.uid);
    if (notebook) {
        notebook.saveRequest = dateUid.result.date;
    }
    return {
        ...state,
        notebooks,
    };
})
    .case(notebookActions.insertAbove.done, (state, _) => {
    return state;
})
    .case(notebookActions.insertBelow.done, (state, _) => {
    return state;
})
    .case(notebookActions.changeCellType.done, (state, _) => {
    return state;
})
    .case(notebookActions.run.done, (state, _) => {
    return state;
})
    .case(notebookActions.delete.done, (state, _) => {
    return state;
});
//# sourceMappingURL=NotebookState.js.map