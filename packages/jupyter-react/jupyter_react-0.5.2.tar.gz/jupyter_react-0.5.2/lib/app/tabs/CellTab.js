import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { ActionList, Avatar, ActionMenu, ProgressBar, Box } from '@primer/react';
import { LinkIcon } from '@primer/octicons-react';
import { DatalayerGreenIcon } from "@datalayer/icons-react";
const CellTab = () => {
    return (_jsxs(_Fragment, { children: [_jsxs(ActionMenu, { children: [_jsx(ActionMenu.Button, { children: "Cells" }), _jsx(ActionMenu.Overlay, { children: _jsxs(ActionList, { children: [_jsx(ActionList.Item, { onSelect: event => console.log('New cell'), children: "New cell" }), _jsx(ActionList.Item, { children: "Copy cell" }), _jsx(ActionList.Item, { children: "Edit cell" }), _jsx(ActionList.Divider, {}), _jsx(ActionList.Item, { variant: "danger", children: "Delete cell" })] }) })] }), _jsxs(ActionList, { children: [_jsxs(ActionList.Item, { children: [_jsx(ActionList.LeadingVisual, { children: _jsx(DatalayerGreenIcon, {}) }), "Dask kernel"] }), _jsx(Box, { borderColor: "border.default", borderBottomWidth: 1, borderBottomStyle: "solid", pb: 3 }), _jsxs(ActionList.Item, { children: [_jsx(ActionList.LeadingVisual, { children: _jsx(LinkIcon, {}) }), "Starting..."] }), _jsx(ProgressBar, { progress: 80 }), _jsx(Box, { borderColor: "border.default", borderBottomWidth: 1, borderBottomStyle: "solid", pb: 3 }), _jsxs(ActionList.Item, { children: [_jsx(ActionList.LeadingVisual, { children: _jsx(Avatar, { src: "https://github.com/mona.png" }) }), "Me"] })] })] }));
};
export default CellTab;
//# sourceMappingURL=CellTab.js.map