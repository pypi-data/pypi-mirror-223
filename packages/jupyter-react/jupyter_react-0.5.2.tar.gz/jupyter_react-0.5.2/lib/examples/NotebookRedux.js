import { jsxs as _jsxs, jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import { useDispatch } from "react-redux";
import { Box, Button } from '@primer/react';
import Jupyter from '../jupyter/Jupyter';
import Notebook from '../components/notebook/Notebook';
import CellSidebarDefault from "../components/notebook/cell/sidebar/CellSidebarDefault";
import NotebookToolbar from "./toolbars/NotebookToolbar";
import { createReduxEpicStore, createInjectableStore } from '../redux/Store';
import { exampleReducer, selectFoo, exampleActions } from './redux/ExampleState';
import notebookExample from "./notebooks/NotebookExample1.ipynb.json";
import "./../../style/index.css";
const store = createReduxEpicStore();
const injectableStore = createInjectableStore(store);
injectableStore.inject('init', exampleReducer);
const FooDisplay = () => {
    const foo = selectFoo();
    return (_jsxs(Box, { m: 3, children: ["Foo date: ", foo ? foo.toISOString() : ""] }));
};
const FooAction = () => {
    const dispatch = useDispatch();
    return (_jsx(Box, { m: 3, children: _jsx(Button, { onClick: () => dispatch(exampleActions.updateFoo(new Date())), children: "Update the current date" }) }));
};
const NotebookRedux = (props) => {
    const { injectableStore } = props;
    return (_jsx(_Fragment, { children: _jsxs(Jupyter, { injectableStore: injectableStore, startDefaultKernel: true, terminals: false, children: [_jsx(FooDisplay, {}), _jsx(FooAction, {}), _jsx(Notebook, { nbformat: notebookExample, CellSidebar: CellSidebarDefault, Toolbar: NotebookToolbar, height: 'calc(100vh - 2.6rem)' // (Height - Toolbar Height).
                    , cellSidebarMargin: 120, uid: "notebook-uid-1" })] }) }));
};
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(NotebookRedux, { injectableStore: injectableStore }));
//# sourceMappingURL=NotebookRedux.js.map