import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useMemo, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { ActionMenu, ActionList, Box, IconButton, ProgressBar } from '@primer/react';
import { KebabHorizontalIcon, StopIcon, PaintbrushIcon } from '@primer/octicons-react';
import { UUID } from '@lumino/coreutils';
import OutputAdapter from './OutputAdapter';
import { selectExecute, outputActions, outputReducer } from './OutputState';
import { useJupyter } from "../../jupyter/JupyterContext";
import Lumino from '../../jupyter/lumino/Lumino';
import CodeMirrorEditor from '../codemirror/CodeMirrorEditor';
import OutputRenderer from './OutputRenderer';
import './Output.css';
const KernelProgressMenu = (props) => {
    const { outputAdapter } = props;
    return (_jsxs(ActionMenu, { children: [_jsx(ActionMenu.Anchor, { children: _jsx(IconButton, { "aria-labelledby": "", icon: KebabHorizontalIcon, variant: "invisible" }) }), _jsx(ActionMenu.Overlay, { children: _jsxs(ActionList, { children: [_jsxs(ActionList.Item, { onSelect: e => { e.preventDefault(); outputAdapter.interrupt(); }, children: [_jsx(ActionList.LeadingVisual, { children: _jsx(StopIcon, {}) }), "Interrupt kernel"] }), _jsxs(ActionList.Item, { variant: "danger", onClick: e => { e.preventDefault(); outputAdapter.clearOutput(); }, children: [_jsx(ActionList.LeadingVisual, { children: _jsx(PaintbrushIcon, {}) }), "Clear outputs"] })] }) })] }));
};
const KernelProgressBar = () => {
    const [progress, setProgress] = useState(0);
    useEffect(() => {
        const interval = setInterval(() => {
            setProgress((oldValue) => {
                let newValue = oldValue + 1;
                if (newValue > 100) {
                    newValue = 0;
                }
                return newValue;
            });
        }, 100);
        return () => clearInterval(interval);
    }, []);
    return (_jsx(ProgressBar, { progress: progress, barSize: "small" }));
};
export const Output = (props) => {
    const { injectableStore, defaultKernel: kernel } = useJupyter();
    const { sourceId, autoRun, code, showEditor, clearTrigger, executeTrigger, adapter, receipt, disableRun, insertText, toolbarPosition, codePre, luminoWidgets: useLumino } = props;
    const dispatch = useDispatch();
    const [id, setId] = useState(sourceId);
    const [kernelStatus, setKernelStatus] = useState('unknown');
    const [outputAdapter, setOutputAdapter] = useState();
    const [outputs, setOutputs] = useState(props.outputs);
    useMemo(() => {
        injectableStore.inject('output', outputReducer);
    }, [sourceId]);
    useEffect(() => {
        if (!id) {
            setId(UUID.uuid4());
        }
    }, []);
    useEffect(() => {
        if (id && kernel) {
            const outputAdapter = adapter || new OutputAdapter(kernel, outputs || []);
            if (receipt) {
                outputAdapter.outputArea.model.changed.connect((sender, change) => {
                    if (change.type === 'add') {
                        change.newValues.map(val => {
                            if (val && val.data) {
                                const out = val.data['text/html']; // val.data['application/vnd.jupyter.stdout'];
                                if (out) {
                                    if (out.indexOf(receipt) > -1) {
                                        dispatch(outputActions.grade({
                                            sourceId,
                                            success: true,
                                        }));
                                    }
                                }
                            }
                        });
                    }
                });
            }
            setOutputAdapter(outputAdapter);
            outputAdapter.outputArea.model.changed.connect((outputModel, args) => {
                setOutputs(outputModel.toJSON());
            });
        }
    }, [id, kernel]);
    useEffect(() => {
        if (outputAdapter) {
            if (!outputAdapter.kernel) {
                outputAdapter.kernel = kernel;
            }
            if (autoRun) {
                outputAdapter.execute(code);
            }
        }
    }, [outputAdapter]);
    useEffect(() => {
        if (kernel) {
            kernel.connection.then((kernelConnection) => {
                setKernelStatus(kernelConnection.status);
                kernelConnection.statusChanged.connect((kernelConnection, status) => {
                    setKernelStatus(status);
                });
            });
            return () => {
                //        kernel.connection.then(k => k.shutdown().then(() => console.log(`Kernel ${k.id} is terminated.`)));
            };
        }
    }, [kernel]);
    const executeRequest = selectExecute(sourceId);
    useEffect(() => {
        if (outputAdapter && executeRequest && executeRequest.sourceId === id) {
            outputAdapter.execute(executeRequest.source);
        }
    }, [executeRequest, outputAdapter]);
    useEffect(() => {
        if (outputAdapter && executeTrigger > 0) {
            outputAdapter.execute(code);
        }
    }, [executeTrigger]);
    useEffect(() => {
        if (outputAdapter && clearTrigger > 0) {
            outputAdapter.clearOutput();
        }
    }, [clearTrigger, outputAdapter]);
    return (_jsxs(_Fragment, { children: [showEditor && outputAdapter && id &&
                _jsx(Box, { sx: {
                        '& .cm-editor': {
                            borderRadius: '5px',
                        },
                    }, children: _jsx(CodeMirrorEditor, { autoRun: autoRun, code: code, codePre: codePre, kernel: kernel, outputAdapter: outputAdapter, sourceId: id, disableRun: disableRun, insertText: insertText, toolbarPosition: toolbarPosition }) }), outputAdapter &&
                _jsxs(Box, { display: "flex", children: [_jsx(Box, { flexGrow: 1, children: kernelStatus !== 'idle' && _jsx(KernelProgressBar, {}) }), _jsx(Box, { style: { marginTop: "-13px" }, children: _jsx(KernelProgressMenu, { outputAdapter: outputAdapter }) })] }), outputs &&
                _jsx(Box, { sx: {
                        '& .jp-OutputArea': {
                            fontSize: '10px',
                        },
                        '& .jp-OutputPrompt': {
                        //              display: 'none',
                        },
                        '& .jp-OutputArea-prompt': {
                            display: 'none',
                            //              width: '0px',
                        },
                        '& pre': {
                            fontSize: '12px',
                            wordBreak: 'break-all',
                            wordWrap: 'break-word',
                            whiteSpace: 'pre-wrap',
                        },
                    }, children: useLumino
                        ?
                            (outputAdapter &&
                                _jsx(Lumino, { children: outputAdapter.outputArea }))
                        :
                            (outputs &&
                                _jsx(_Fragment, { children: outputs.map((output) => {
                                        return _jsx(OutputRenderer, { output: output });
                                    }) })) })] }));
};
Output.defaultProps = {
    outputs: [
        {
            "output_type": "execute_result",
            "data": {
                "text/html": [
                    "<p>Type code in the cell and Shift+Enter to execute.</p>"
                ]
            },
            "execution_count": 0,
            "metadata": {},
        }
    ],
    disableRun: false,
    toolbarPosition: 'up',
    executeTrigger: 0,
    clearTrigger: 0,
    luminoWidgets: true,
};
export default Output;
//# sourceMappingURL=Output.js.map