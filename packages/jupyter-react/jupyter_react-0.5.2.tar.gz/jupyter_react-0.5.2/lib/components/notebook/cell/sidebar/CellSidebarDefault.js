import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { ActionMenu, Button, Box } from "@primer/react";
import { ChevronRightIcon, XIcon, ChevronUpIcon, ChevronDownIcon, SquareIcon } from "@primer/octicons-react";
import { notebookActions, selectActiveCell } from '../../NotebookState';
import CellMetadataEditor from '../metadata/CellMetadataEditor';
import { DATALAYER_CELL_HEADER_CLASS } from './lumino/CellSidebarWidget';
export const CellSidebarDefault = (props) => {
    const { notebookId, cellId, nbgrader } = props;
    const [visible, setVisible] = useState(false);
    const dispatch = useDispatch();
    const activeCell = selectActiveCell(notebookId);
    const layout = (activeCell?.layout);
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
    return activeCell ?
        (_jsxs(Box, { className: DATALAYER_CELL_HEADER_CLASS, sx: {
                '& p': {
                    marginBottom: '0 !important',
                }
            }, children: [_jsx("span", { style: { display: "flex" }, children: _jsx(Button, { leadingVisual: ChevronRightIcon, variant: "invisible", size: "small", onClick: (e) => {
                            e.preventDefault();
                            dispatch(notebookActions.run.started(notebookId));
                        }, children: "Run" }) }), _jsx("span", { style: { display: "flex" }, children: _jsx(Button, { leadingVisual: ChevronUpIcon, variant: "invisible", size: "small", onClick: (e) => {
                            e.preventDefault();
                            dispatch(notebookActions.insertAbove.started({ uid: notebookId, cellType: "code" }));
                        }, children: "Code" }) }), _jsx("span", { style: { display: "flex" }, children: _jsx(Button, { leadingVisual: ChevronUpIcon, variant: "invisible", size: "small", onClick: (e) => {
                            e.preventDefault();
                            dispatch(notebookActions.insertAbove.started({ uid: notebookId, cellType: "markdown" }));
                        }, children: "Markdown" }) }), _jsx("span", { style: { display: "flex" }, children: activeCell.model.type === "code" ?
                        _jsx(Button, { leadingVisual: SquareIcon, variant: "invisible", size: "small", onClick: (e) => {
                                e.preventDefault();
                                dispatch(notebookActions.changeCellType.started({ uid: notebookId, cellType: "markdown" }));
                            }, children: "To Markdown" })
                        :
                            _jsx(Button, { leadingVisual: SquareIcon, variant: "invisible", size: "small", onClick: (e) => {
                                    e.preventDefault();
                                    dispatch(notebookActions.changeCellType.started({ uid: notebookId, cellType: "code" }));
                                }, children: "To Code" }) }), _jsx("span", { style: { display: "flex" }, children: _jsx(Button, { leadingVisual: ChevronDownIcon, variant: "invisible", size: "small", onClick: (e) => {
                            e.preventDefault();
                            dispatch(notebookActions.insertBelow.started({ uid: notebookId, cellType: "markdown" }));
                        }, children: "Markdown" }) }), _jsx("span", { style: { display: "flex" }, children: _jsx(Button, { leadingVisual: ChevronDownIcon, variant: "invisible", size: "small", onClick: (e) => {
                            e.preventDefault();
                            dispatch(notebookActions.insertBelow.started({ uid: notebookId, cellType: "code" }));
                        }, children: "Code" }) }), _jsx("span", { style: { display: "flex" }, children: _jsx(Button, { leadingVisual: XIcon, variant: "invisible", size: "small", onClick: (e) => {
                            e.preventDefault();
                            dispatch(notebookActions.delete.started(notebookId));
                        }, children: "Delete" }) }), nbgrader &&
                    _jsx(ActionMenu, { children: _jsx(CellMetadataEditor, { notebookId: notebookId, cell: activeCell, nbgrader: nbgrader }) })] }))
        :
            (_jsx(_Fragment, {}));
};
export default CellSidebarDefault;
//# sourceMappingURL=CellSidebarDefault.js.map