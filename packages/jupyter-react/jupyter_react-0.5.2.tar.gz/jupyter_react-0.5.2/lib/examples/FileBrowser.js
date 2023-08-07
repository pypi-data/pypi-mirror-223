import { jsx as _jsx } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import Jupyter from '../jupyter/Jupyter';
import FileBrowser from "../components/filebrowser/FileBrowser";
import "./../../style/index.css";
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(Jupyter, { lite: false, terminals: true, children: _jsx(FileBrowser, {}) }));
//# sourceMappingURL=FileBrowser.js.map