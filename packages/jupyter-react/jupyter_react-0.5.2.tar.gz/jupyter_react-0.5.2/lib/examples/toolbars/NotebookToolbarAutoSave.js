import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { notebookActions, selectNotebook, } from '../../components/notebook/NotebookState';
import { PlusIcon, PlayIcon, StopIcon, TrashIcon } from '@primer/octicons-react';
import { IconButton } from '@primer/react';
import { cmdIds } from '../../components/notebook/NotebookCommands';
import { Button, ButtonGroup } from '@primer/react';
const NotebookToolbarAutoSave = (props) => {
    const { notebookId } = props;
    const [addtype, setaddtype] = useState('code');
    const dispatch = useDispatch();
    const notebook = selectNotebook(notebookId);
    const notebookState = useSelector((state) => state.notebook);
    useEffect(() => {
        notebookState.notebooks
            .get(notebookId)
            ?.adapter?.commands.execute(cmdIds.save);
    }, [notebookState]);
    const handleChangeCellType = (newType) => {
        setaddtype(newType);
    };
    return (_jsxs("div", { style: {
            display: 'flex',
            width: '100%',
            borderBottom: '0.1rem solid lightgrey',
            position: 'relative',
            zIndex: '1',
            backgroundColor: 'white',
            top: '0',
        }, children: [_jsxs("div", { style: {
                    display: 'flex',
                    width: '50%',
                    paddingLeft: '7vw',
                    gap: '0.75vw',
                }, children: [_jsx(IconButton, { size: "small", color: "primary", "aria-label": "Insert Cell", onClick: e => {
                            e.preventDefault();
                            if (addtype === 'raw')
                                dispatch(notebookActions.insertBelow.started({
                                    uid: notebookId,
                                    cellType: 'raw',
                                }));
                            else if (addtype === 'code')
                                dispatch(notebookActions.insertBelow.started({
                                    uid: notebookId,
                                    cellType: 'code',
                                }));
                            else if (addtype === 'markdown')
                                dispatch(notebookActions.insertBelow.started({
                                    uid: notebookId,
                                    cellType: 'markdown',
                                }));
                        }, style: { color: 'grey' }, icon: PlusIcon }), _jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Run Cell", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.run.started(notebookId));
                        }, style: { color: 'grey' }, icon: PlayIcon }), notebook?.kernelStatus === 'idle' && (_jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Run All Cells", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.runAll.started(notebookId));
                        }, style: { color: 'grey' }, icon: PlayIcon })), notebook?.kernelStatus === 'busy' && (_jsx(IconButton, { size: "small", color: "error", "aria-label": "Interrupt", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.interrupt.started(notebookId));
                        }, icon: StopIcon })), _jsx(IconButton, { size: "small", color: "error", "aria-label": "Delete", onClick: e => {
                            e.preventDefault();
                            dispatch(notebookActions.delete.started(notebookId));
                        }, icon: TrashIcon })] }), _jsx("div", { style: {
                    display: 'flex',
                    width: '50%',
                    paddingRight: '7vw',
                    gap: '0.75vw',
                    justifyContent: 'flex-end',
                    alignItems: 'center',
                }, children: _jsxs(ButtonGroup, { children: [_jsx(Button, { variant: addtype == 'code' ? 'primary' : 'invisible', onClick: () => handleChangeCellType('code'), size: "small", children: "Code" }), _jsx(Button, { variant: addtype == 'markdown' ? 'primary' : 'invisible', onClick: () => handleChangeCellType('markdown'), size: "small", children: "Markdown" }), _jsx(Button, { variant: addtype == 'raw' ? 'primary' : 'invisible', onClick: () => handleChangeCellType('raw'), size: "small", children: "Raw" })] }) })] }));
};
export default NotebookToolbarAutoSave;
//# sourceMappingURL=NotebookToolbarAutoSave.js.map