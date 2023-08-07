import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { ThemeProvider, BaseStyles, Box } from '@primer/react';
import { CpuIcon } from '@primer/octicons-react';
import { UnderlineNav } from '@primer/react/drafts';
import CellTab from './tabs/CellTab';
const JupyterReact = () => {
    const [tab, setTab] = useState(1);
    return (_jsx(_Fragment, { children: _jsx(ThemeProvider, { children: _jsx(BaseStyles, { children: _jsxs(Box, { style: { maxWidth: 700 }, children: [_jsx(Box, { mb: 3, children: _jsx(UnderlineNav, { children: _jsx(UnderlineNav.Item, { "aria-current": "page", icon: CpuIcon, onSelect: e => { e.preventDefault(); setTab(1); }, children: "Cell" }) }) }), _jsx(Box, { children: (tab === 1) && _jsx(CellTab, {}) })] }) }) }) }));
};
export default JupyterReact;
//# sourceMappingURL=JupyterReact.js.map