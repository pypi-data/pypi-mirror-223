import { jsx as _jsx } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import Jupyter from '../jupyter/Jupyter';
import Notebook from '../components/notebook/Notebook';
import NotebookToolbar from "./toolbars/NotebookToolbar";
import CellSidebarDefault from "../components/notebook/cell/sidebar/CellSidebarDefault";
import "./../../style/index.css";
const NotebookExample = () => (_jsx(Jupyter, { lite: false, useRunningKernelIndex: -1, startDefaultKernel: true, terminals: false, children: _jsx(Notebook, { path: "bokeh.ipynb", CellSidebar: CellSidebarDefault, Toolbar: NotebookToolbar, height: 'calc(100vh - 2.6rem)' // (Height - Toolbar Height).
        , cellSidebarMargin: 120, uid: "notebook-uid" }) }));
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(NotebookExample, {}));
//# sourceMappingURL=Bokeh.js.map