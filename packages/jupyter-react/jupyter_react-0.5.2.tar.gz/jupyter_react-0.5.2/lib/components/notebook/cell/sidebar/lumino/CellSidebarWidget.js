import { jsx as _jsx } from "react/jsx-runtime";
import { createElement } from 'react';
import { createPortal } from 'react-dom';
import { newUuid } from '../../../../../jupyter/utils/Ids';
import { LuminoReactPortal } from '../../../../../jupyter/lumino/LuminoReactPortal';
import { notebookActions } from '../../../NotebookState';
export const DATALAYER_CELL_HEADER_CLASS = 'dla-CellHeader-Container';
export class CellSidebarWidget extends LuminoReactPortal {
    commands;
    constructor(CellSidebar, notebookId, nbgrader, commands, store) {
        super();
        this.commands = commands;
        this.addClass('jp-CellHeader');
        this.id = newUuid();
        const props = {
            notebookId,
            cellId: this.id,
            command: this.commands,
            nbgrader,
        };
        const sidebar = createElement(CellSidebar, props);
        const portal = createPortal(_jsx("div", { className: DATALAYER_CELL_HEADER_CLASS, children: sidebar }), this.node);
        store.dispatch(notebookActions.addPortals({ uid: notebookId, portals: [portal] }));
    }
}
export default CellSidebarWidget;
//# sourceMappingURL=CellSidebarWidget.js.map