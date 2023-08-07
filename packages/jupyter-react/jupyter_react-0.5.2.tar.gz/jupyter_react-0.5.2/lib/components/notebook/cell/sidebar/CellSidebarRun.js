import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Box, Button } from '@primer/react';
import { PlayIcon } from "@primer/octicons-react";
import { notebookActions, selectActiveCell } from '../../NotebookState';
import { DATALAYER_CELL_HEADER_CLASS } from './lumino/CellSidebarWidget';
export const CellSidebarRun = (props) => {
    const { notebookId } = props;
    const [visible, setVisible] = useState(false);
    const dispatch = useDispatch();
    const activeCell = selectActiveCell(notebookId);
    const layout = (activeCell?.layout);
    if (layout) {
        const cellWidget = layout.widgets[0];
        if (!visible && (cellWidget?.node.id === props.cellId)) {
            setVisible(true);
        }
        if (visible && (cellWidget?.node.id !== props.cellId)) {
            setVisible(false);
        }
    }
    if (!visible) {
        return _jsx("div", {});
    }
    return (activeCell ?
        _jsx(Box, { className: DATALAYER_CELL_HEADER_CLASS, sx: {
                '& p': {
                    marginBottom: '0 !important',
                }
            }, children: _jsx("span", { style: { display: "flex" }, children: _jsx(Button, { trailingVisual: PlayIcon, size: "small", variant: "invisible", onClick: (e) => {
                        e.preventDefault();
                        dispatch(notebookActions.run.started(notebookId));
                    }, children: "Run" }) }) })
        :
            _jsx(_Fragment, {}));
};
export default CellSidebarRun;
//# sourceMappingURL=CellSidebarRun.js.map