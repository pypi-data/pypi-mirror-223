import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect, useMemo } from 'react';
import { useDispatch } from "react-redux";
import TerminalAdapter from './TerminalAdapter';
import { terminalActions, terminalReducer } from './TerminalState';
import { useJupyter } from './../../jupyter/JupyterContext';
import Lumino from '../../jupyter/lumino/Lumino';
export const Terminal = () => {
    const { injectableStore } = useJupyter();
    const dispatch = useDispatch();
    const [adapter, setAdapter] = useState();
    useMemo(() => {
        injectableStore.inject('terminal', terminalReducer);
    }, []);
    useEffect(() => {
        const adapter = new TerminalAdapter();
        dispatch(terminalActions.update({ adapter }));
        setAdapter(adapter);
    }, []);
    return adapter
        ?
            _jsx(Lumino, { children: adapter.panel })
        :
            _jsx(_Fragment, { children: "Loading Jupyter Terminal..." });
};
export default Terminal;
//# sourceMappingURL=Terminal.js.map