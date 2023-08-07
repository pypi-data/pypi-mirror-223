import { jsx as _jsx } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import Jupyter from '../jupyter/Jupyter';
import Terminal from "../components/terminal/Terminal";
import "./../../style/index.css";
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(Jupyter, { lite: false, terminals: true, children: _jsx(Terminal, {}) }));
//# sourceMappingURL=Terminal.js.map