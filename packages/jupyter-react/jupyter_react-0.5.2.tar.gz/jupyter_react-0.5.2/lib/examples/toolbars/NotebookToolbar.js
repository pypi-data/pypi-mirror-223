import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button, ButtonGroup, IconButton } from '@primer/react';
import { PlusIcon, ChevronRightIcon, StopIcon, FileAddedIcon, TrashIcon, SyncIcon, } from '@primer/octicons-react';
import { FastForwardIcon } from '@datalayer/icons-react';
import { cmdIds } from '../../components/notebook/NotebookCommands';
import { notebookActions, selectNotebook, selectSaveRequest, } from '../../components/notebook/NotebookState';
const NotebookToolbar = (props) => {
    const { notebookId } = props;
    const [autoSave, setAutoSave] = useState(false);
    const [addType, setAddType] = useState('code');
    const dispatch = useDispatch();
    const notebook = selectNotebook(notebookId);
    const saveRequest = selectSaveRequest(notebookId);
    const notebookstate = useSelector((state) => {
        return state.notebook;
    });
    useEffect(() => {
        notebook?.adapter?.commands.execute(cmdIds.save);
    }, [saveRequest]);
    useEffect(() => {
        if (autoSave) {
            notebook?.adapter?.commands.execute(cmdIds.save);
        }
    }, [notebookstate]);
    const handleChangeCellType = (newType) => {
        setAddType(newType);
    };
    return (_jsxs("div", { style: {
            display: 'flex',
            width: '100%',
            borderBottom: '0.1rem solid lightgrey',
            position: 'relative',
            zIndex: '1',
            backgroundColor: 'white',
            top: '0',
            padding: '0.25rem 0',
        }, children: [_jsxs("div", { style: {
                    display: 'flex',
                    width: '50%',
                    paddingLeft: '7vw',
                    gap: '0.75vw',
                    alignItems: 'center',
                }, children: [_jsx(IconButton, { variant: "invisible", size: "small", color: "primary", "aria-label": "Save", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.save.started({ uid: notebookId, date: new Date() }));
                        }, icon: FileAddedIcon }), _jsx(IconButton, { variant: "invisible", size: "small", color: "primary", "aria-label": "Insert Cell", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.insertBelow.started({
                                uid: notebookId,
                                cellType: addType,
                            }));
                        }, icon: PlusIcon }), _jsx(IconButton, { variant: "invisible", size: "small", color: "secondary", "aria-label": "Run Cell", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.run.started(notebookId));
                        }, icon: ChevronRightIcon }), notebook?.kernelStatus === 'idle' ?
                        _jsx(IconButton, { variant: "invisible", size: "small", color: "secondary", "aria-label": "Run All Cells", onClick: e => {
                                e.preventDefault();
                                dispatch(notebookActions.runAll.started(notebookId));
                            }, icon: FastForwardIcon })
                        :
                            _jsx(IconButton, { variant: "invisible", size: "small", color: "error", "aria-label": "Interrupt", onClick: e => {
                                    e.preventDefault();
                                    dispatch(notebookActions.interrupt.started(notebookId));
                                }, icon: StopIcon }), _jsx(IconButton, { variant: "invisible", size: "small", color: "error", "aria-label": "Delete", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.delete.started(notebookId));
                        }, icon: TrashIcon })] }), _jsxs("div", { style: {
                    display: 'flex',
                    width: '50%',
                    paddingRight: '7vw',
                    gap: '0.75vw',
                    justifyContent: 'flex-end',
                    alignItems: 'center',
                }, children: [_jsx(IconButton, { "aria-label": "Auto Save", variant: autoSave ? 'primary' : 'invisible', onClick: e => {
                            e.preventDefault();
                            setAutoSave(!autoSave);
                        }, size: "small", color: autoSave ? 'success' : 'error', icon: SyncIcon }), _jsxs(ButtonGroup, { children: [_jsx(Button, { variant: addType == 'code' ? 'primary' : 'invisible', onClick: () => handleChangeCellType('code'), size: "small", children: "Code" }), _jsx(Button, { variant: addType == 'markdown' ? 'primary' : 'default', onClick: () => handleChangeCellType('markdown'), size: "small", children: "Markdown" }), _jsx(Button, { variant: addType == 'raw' ? 'primary' : 'invisible', onClick: () => handleChangeCellType('raw'), size: "small", children: "Raw" })] })] })] }));
};
export default NotebookToolbar;
//# sourceMappingURL=NotebookToolbar.js.map