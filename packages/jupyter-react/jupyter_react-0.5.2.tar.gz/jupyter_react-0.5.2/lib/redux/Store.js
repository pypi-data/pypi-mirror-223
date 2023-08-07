import { applyMiddleware, combineReducers, createStore } from "redux";
import { createEpicMiddleware } from "redux-observable";
import { initReducer } from "./InitState";
const epicMiddleware = createEpicMiddleware();
function createReducer(asyncReducers) {
    return combineReducers({
        ...asyncReducers,
    });
}
/*
export const createEpics = (initEpics: any) => {
  const epic$ = new BehaviorSubject(initEpics);
  const rootEpic = (action$: any, state$: any, deps: any) => epic$.pipe(
    mergeMap(epic => epic(action$, state$, deps))
  );
  epicMiddleware.run(rootEpic as any);
}
*/
export const createInjectableStore = (store) => {
    const injectableStore = store;
    injectableStore.asyncReducers = {};
    injectableStore.inject = (key, asyncReducer, epic) => {
        const reducer = injectableStore.asyncReducers[key];
        if (key === 'init' || !reducer) {
            if (epic) {
                epicMiddleware.run(epic);
            }
            injectableStore.asyncReducers[key] = asyncReducer;
            const newReducer = createReducer(injectableStore.asyncReducers);
            injectableStore.replaceReducer(newReducer);
        }
    };
    return injectableStore;
};
export const createReduxEpicStore = () => createStore(createReducer({ initReducer }), applyMiddleware(epicMiddleware));
const store = createReduxEpicStore();
const injectableStore = createInjectableStore(store);
injectableStore.inject('init', initReducer);
export default injectableStore;
//# sourceMappingURL=Store.js.map