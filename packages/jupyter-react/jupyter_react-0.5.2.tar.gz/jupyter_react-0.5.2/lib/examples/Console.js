import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import { Box } from '@primer/react';
import Jupyter from '../jupyter/Jupyter';
import Console from '../components/console/Console';
import "./../../style/index.css";
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsxs(Jupyter, { lite: true, children: [_jsx(Box, { as: "h1", children: "A Jupyter Console" }), _jsx(Console, {})] }));
//# sourceMappingURL=Console.js.map