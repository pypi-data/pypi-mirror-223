import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { createRoot } from 'react-dom/client';
import { Box, Button, ButtonGroup } from '@primer/react';
import Jupyter from '../jupyter/Jupyter';
import { useJupyter } from '../jupyter/JupyterContext';
import Kernel from '../jupyter/services/kernel/Kernel';
import Notebook from '../components/notebook/Notebook';
import CellSidebarDefault from '../components/notebook/cell/sidebar/CellSidebarDefault';
import notebookExample from './notebooks/NotebookExample1.ipynb.json';
import "./../../style/index.css";
const NotebookUnmount = () => {
    const [showNotebook, setShowNotebook] = useState(false);
    const [kernel, setKernel] = useState();
    const { kernelManager } = useJupyter();
    useEffect(() => {
        if (kernelManager) {
            const kernel = new Kernel({ kernelManager, kernelName: "python" });
            setKernel(kernel);
            setShowNotebook(true);
        }
    }, [kernelManager]);
    useEffect(() => {
        if (!showNotebook && kernel) {
            kernel.shutdown();
        }
    }, [showNotebook]);
    const unmount = () => {
        setShowNotebook(false);
    };
    return (_jsx(_Fragment, { children: (showNotebook && kernel) ?
            (_jsxs(_Fragment, { children: [_jsx(Box, { display: "flex", children: _jsx(ButtonGroup, { children: _jsx(Button, { variant: "default", size: "small", onClick: unmount, children: "Unmount" }) }) }), _jsx(Notebook, { nbformat: notebookExample, 
                        //                kernel={kernel}
                        CellSidebar: CellSidebarDefault, height: "700px", uid: "notebook-unmount-id" })] }))
            :
                _jsxs(_Fragment, { children: [_jsx(Box, { children: "The Notebook React.js component is not mounted." }), _jsx(Box, { children: "The connections to the Kernel should not happen any more - Check the Network tab in your Browser Devtools." })] }) }));
};
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(Jupyter, { lite: false, terminals: true, startDefaultKernel: true, children: _jsx(NotebookUnmount, {}) }));
//# sourceMappingURL=NotebookUnmount.js.map