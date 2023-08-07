import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import { Box } from '@primer/react';
import Jupyter from '../jupyter/Jupyter';
import Cell from '../components/cell/Cell';
import "./../../style/index.css";
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsxs(Jupyter, { lite: false, children: [_jsx(Box, { as: "h1", children: "Jupyter Cells wrapped in a single Jupyter Context" }), _jsx(Cell, { source: "x=1" }), _jsx(Cell, { source: "print(x)" }), _jsx(Cell, { source: `import random

r = random.randint(0,9)` }), _jsx(Cell, { source: "print(f'Random integer: {r}')" })] }));
//# sourceMappingURL=Cells.js.map