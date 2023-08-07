import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState, useMemo } from 'react';
import { useTheme, ActionMenu, ActionList, IconButton, Box } from '@primer/react';
import { KebabHorizontalIcon, ArrowRightIcon, StopIcon, PaintbrushIcon } from '@primer/octicons-react';
const CodeMirrorOutputToolbarMenu = (props) => {
    const { executeCode, outputAdapter, editorView } = props;
    return (_jsxs(ActionMenu, { children: [_jsx(ActionMenu.Anchor, { children: _jsx(IconButton, { "aria-labelledby": "", icon: KebabHorizontalIcon, variant: "invisible" }) }), _jsx(ActionMenu.Overlay, { children: _jsxs(ActionList, { children: [_jsxs(ActionList.Item, { onSelect: e => { e.preventDefault(); executeCode(editorView); }, children: [_jsx(ActionList.LeadingVisual, { children: _jsx(ArrowRightIcon, {}) }), _jsx(ActionList.TrailingVisual, { children: "\u21E7 \u21B5" }), "Run code"] }), _jsxs(ActionList.Item, { onSelect: e => { e.preventDefault(); outputAdapter.interrupt(); }, children: [_jsx(ActionList.LeadingVisual, { children: _jsx(StopIcon, {}) }), "Interrupt kernel"] }), _jsxs(ActionList.Item, { variant: "danger", onClick: e => { e.preventDefault(); outputAdapter.clearOutput(); }, children: [_jsx(ActionList.LeadingVisual, { children: _jsx(PaintbrushIcon, {}) }), "Clear outputs"] })] }) })] }));
};
const KernelStatus = ({ color }) => (_jsx(Box, { sx: { backgroundColor: color, width: '14px', height: '14px', borderRadius: 3 } }));
export const CodeMirrorOutputToolbar = (props) => {
    const { executeCode, editorView, kernel, codePre } = props;
    const { theme } = useTheme();
    const okColor = useMemo(() => theme?.colorSchemes.light.colors.success.muted, []);
    const nokColor = useMemo(() => theme?.colorSchemes.light.colors.severe.muted, []);
    const [kernelStatus, setKernelStatus] = useState('unknown');
    useEffect(() => {
        if (kernel) {
            kernel.connection.then((kernelConnection) => {
                if (codePre) {
                    executeCode(editorView, codePre);
                }
                setKernelStatus(kernelConnection.status);
                kernelConnection.statusChanged.connect((kernelConnection, status) => {
                    setKernelStatus(status);
                });
            });
        }
    }, [kernel]);
    const getKernelStatusColor = (status) => {
        if (status === "idle") {
            return okColor;
        }
        return nokColor;
    };
    return (_jsxs(Box, { display: "flex", children: [_jsx(Box, { flexGrow: 1 }), _jsx(Box, { sx: { paddingTop: '6px' }, children: _jsx(KernelStatus, { color: getKernelStatusColor(kernelStatus) }) }), _jsx(Box, { children: _jsx(CodeMirrorOutputToolbarMenu, { ...props }) })] }));
};
export default CodeMirrorOutputToolbar;
//# sourceMappingURL=CodeMirrorOutputToolbar.js.map