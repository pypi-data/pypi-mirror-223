import { Fragment as _Fragment, jsx as _jsx } from "react/jsx-runtime";
import { useJupyter } from './../../jupyter/JupyterContext';
import Lumino from '../../jupyter/lumino/Lumino';
import ConsoleAdapter from './ConsoleAdapter';
import './Console.css';
export const Console = () => {
    const { serviceManager } = useJupyter();
    if (!serviceManager) {
        return _jsx(_Fragment, { children: "Loading..." });
    }
    const consoleAdapter = new ConsoleAdapter(serviceManager);
    return _jsx(Lumino, { children: consoleAdapter.panel });
};
export default Console;
//# sourceMappingURL=Console.js.map