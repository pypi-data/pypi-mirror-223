import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Box } from '@primer/react';
import { notebookActions, selectActiveCell } from '../../NotebookState';
import { PlayIcon, ChevronUpIcon, ChevronDownIcon, XIcon, } from '@primer/octicons-react';
import { IconButton } from '@primer/react';
import { DATALAYER_CELL_HEADER_CLASS } from './lumino/CellSidebarWidget';
export const CellSidebarNew = (props) => {
    const { notebookId, cellId } = props;
    const [visible, setVisible] = useState(false);
    const dispatch = useDispatch();
    const activeCell = selectActiveCell(notebookId);
    const layout = activeCell?.layout;
    if (layout) {
        const cellWidget = layout.widgets[0];
        if (cellWidget?.node.id === cellId) {
            if (!visible) {
                setVisible(true);
            }
        }
        if (cellWidget?.node.id !== cellId) {
            if (visible) {
                setVisible(false);
            }
        }
    }
    if (!visible) {
        return _jsx("div", {});
    }
    return activeCell ? (_jsxs(Box, { className: DATALAYER_CELL_HEADER_CLASS, sx: {
            '& p': {
                marginBottom: '0 !important',
            },
        }, children: [_jsx("span", { style: { display: 'flex' }, children: _jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Run Cell", onClick: e => {
                        e.preventDefault();
                        dispatch(notebookActions.run.started(notebookId));
                    }, icon: PlayIcon, variant: "invisible" }) }), _jsx("span", { style: { display: 'flex' }, children: _jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Add Code Above", onClick: e => {
                        e.preventDefault();
                        dispatch(notebookActions.insertAbove.started({
                            uid: notebookId,
                            cellType: 'code',
                        }));
                    }, icon: ChevronUpIcon, variant: "invisible" }) }), _jsx("span", { style: { display: 'flex' }, children: _jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Run Cell", onClick: e => {
                        e.preventDefault();
                        dispatch(notebookActions.insertAbove.started({
                            uid: notebookId,
                            cellType: 'markdown',
                        }));
                    }, icon: ChevronUpIcon, variant: "invisible" }) }), _jsx("span", { style: { display: 'flex' } }), _jsx("span", { style: { display: 'flex' }, children: _jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Run Cell", onClick: e => {
                        e.preventDefault();
                        dispatch(notebookActions.insertBelow.started({
                            uid: notebookId,
                            cellType: 'markdown',
                        }));
                    }, icon: ChevronDownIcon, variant: "invisible" }) }), _jsx("span", { style: { display: 'flex' }, children: _jsx(IconButton, { size: "small", color: "secondary", "aria-label": "Run Cell", onClick: e => {
                        e.preventDefault();
                        dispatch(notebookActions.insertBelow.started({
                            uid: notebookId,
                            cellType: 'code',
                        }));
                    }, icon: ChevronDownIcon, variant: "invisible" }) }), _jsx("span", { style: { display: 'flex' }, children: _jsx(IconButton, { size: "small", color: "error", "aria-label": "Delete", onClick: e => {
                        e.preventDefault();
                        dispatch(notebookActions.delete.started(notebookId));
                    }, icon: XIcon, variant: "invisible" }) })] }))
        :
            (_jsx(_Fragment, {}));
};
export default CellSidebarNew;
//# sourceMappingURL=CellSidebarNew.js.map