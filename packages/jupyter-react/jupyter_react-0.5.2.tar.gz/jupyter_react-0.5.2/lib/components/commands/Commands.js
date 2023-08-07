import { jsx as _jsx } from "react/jsx-runtime";
import CommandAdapter from './CommandsAdapter';
import Lumino from '../../jupyter/lumino/Lumino';
export const Commands = () => {
    const commandsAdapter = new CommandAdapter();
    return _jsx(Lumino, { children: commandsAdapter.panel });
};
export default Commands;
//# sourceMappingURL=Commands.js.map