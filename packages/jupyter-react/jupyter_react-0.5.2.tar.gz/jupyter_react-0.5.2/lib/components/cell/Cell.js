import { jsx as _jsx } from "react/jsx-runtime";
import { useState, useEffect, useMemo } from 'react';
import { useDispatch } from "react-redux";
import { CodeCell } from '@jupyterlab/cells';
import { Box } from "@primer/react";
import { cellActions, cellReducer } from './CellState';
import CellAdapter from './CellAdapter';
import Lumino from '../../jupyter/lumino/Lumino';
import { useJupyter } from './../../jupyter/JupyterContext';
const DEFAULT_SOURCE = `from IPython.display import display

for i in range(10):
    display('String {} added to the DOM in separated DIV.'.format(i))`;
export const Cell = (props) => {
    const { source, autoStart } = props;
    const { serverSettings, injectableStore, defaultKernel } = useJupyter();
    const dispatch = useDispatch();
    const [adapter, setAdapter] = useState();
    useMemo(() => {
        injectableStore.inject('cell', cellReducer);
    }, []);
    useEffect(() => {
        if (source && defaultKernel) {
            const adapter = new CellAdapter(source, serverSettings, defaultKernel);
            dispatch(cellActions.update({ adapter }));
            dispatch(cellActions.source(props.source));
            adapter.codeCell.model.contentChanged.connect((cellModel, changedArgs) => {
                dispatch(cellActions.source(cellModel.sharedModel.getSource()));
            });
            adapter.codeCell.outputArea.outputLengthChanged.connect((outputArea, outputsCount) => {
                dispatch(cellActions.outputsCount(outputsCount));
            });
            adapter.sessionContext.initialize().then(() => {
                if (autoStart) {
                    const execute = CodeCell.execute(adapter.codeCell, adapter.sessionContext);
                    execute.then((msg) => {
                        dispatch(cellActions.update({
                            kernelAvailable: true,
                        }));
                    });
                }
            });
            setAdapter(adapter);
        }
    }, [source, defaultKernel]);
    return adapter
        ?
            _jsx(Box, { sx: {
                    '& .dla-JupyterCell': {
                        position: 'relative !important',
                        contain: 'content !important',
                        //            height: '100% !important',
                        //            marginTop: '30px',
                    },
                    '& .jp-Toolbar': {
                        height: 'auto !important',
                        position: 'relative',
                        //            display: 'none',
                    },
                    '& .lm-BoxPanel': {
                        //            height: 'auto !important',
                        //            minHeight: 'auto !important',
                        position: 'relative',
                    },
                    '& .jp-Cell': {
                        //            width: '100%',
                        //            height: '100% !important',
                        position: 'relative',
                    },
                    '& .jp-CodeCell': {
                        height: 'auto !important',
                        position: 'relative',
                        //            top: 'auto !important',
                    },
                    '& .jp-Cell-outputArea': {
                        paddingBottom: '30px',
                    },
                    '& .jp-CodeMirrorEditor': {
                        cursor: 'text !important',
                    },
                }, children: _jsx(Lumino, { children: adapter.panel }) })
        :
            _jsx(Box, { children: "Loading Jupyter Cell..." });
};
Cell.defaultProps = {
    source: DEFAULT_SOURCE,
    autoStart: true,
};
export default Cell;
//# sourceMappingURL=Cell.js.map