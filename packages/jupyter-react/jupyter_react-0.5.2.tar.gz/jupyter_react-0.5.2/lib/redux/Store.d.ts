import { Store, ReducersMapObject } from "redux";
export type InjectableStore = Store & {
    asyncReducers: ReducersMapObject;
    inject: (key: string, asyncReducer: any, epic?: any) => void;
};
export declare const createInjectableStore: (store: Store) => InjectableStore;
export declare const createReduxEpicStore: () => Store<import("redux").EmptyObject & {
    [x: string]: any;
}, import("redux").AnyAction> & {
    dispatch: unknown;
};
declare const injectableStore: InjectableStore;
export default injectableStore;
