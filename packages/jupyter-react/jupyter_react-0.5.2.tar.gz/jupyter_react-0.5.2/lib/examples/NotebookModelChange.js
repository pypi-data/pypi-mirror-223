import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { createRoot } from 'react-dom/client';
import { Box, Button, ButtonGroup } from '@primer/react';
import Jupyter from '../jupyter/Jupyter';
import { useJupyter } from '../jupyter/JupyterContext';
import Notebook from '../components/notebook/Notebook';
import { selectNotebookModel } from '../components/notebook/NotebookState';
import CellSidebarDefault from '../components/notebook/cell/sidebar/CellSidebarDefault';
import notebookExample1 from './notebooks/NotebookExample1.ipynb.json';
import notebookExample2 from './notebooks/NotebookExample2.ipynb.json';
import "./../../style/index.css";
const NOTEBOOK_UID = 'notebook-model-id';
const NotebookModelChange = () => {
    const { injectableStore } = useJupyter();
    const [model, setModel] = useState(notebookExample1);
    const notebookModel = selectNotebookModel(NOTEBOOK_UID);
    console.log('Current notebook model update', notebookModel?.model, notebookModel?.model?.toJSON());
    const changeModel = () => {
        console.log('Current notebook model from store', injectableStore.getState().notebook.notebooks.get(NOTEBOOK_UID)?.model?.toJSON());
        setModel(notebookExample2);
    };
    return (_jsxs(_Fragment, { children: [_jsx(Box, { display: "flex", children: _jsx(ButtonGroup, { children: _jsx(Button, { variant: "default", size: "small", onClick: changeModel, children: "Change Model" }) }) }), _jsx(Notebook, { uid: NOTEBOOK_UID, nbformat: model, CellSidebar: CellSidebarDefault, height: "700px" })] }));
};
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(Jupyter, { lite: false, terminals: true, children: _jsx(NotebookModelChange, {}) }));
//# sourceMappingURL=NotebookModelChange.js.map