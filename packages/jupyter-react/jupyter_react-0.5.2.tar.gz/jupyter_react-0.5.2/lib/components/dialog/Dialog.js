import { jsx as _jsx } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import LuminoDetached from '../../jupyter/lumino/LuminoDetached';
import DialogAdapter from './DialogAdapter';
export const Dialog = () => {
    const [dialogAdapter, _] = useState(new DialogAdapter());
    useEffect(() => {
        dialogAdapter.dialog.launch().then(success => success);
    }, []);
    return _jsx(LuminoDetached, { children: dialogAdapter.dialog });
};
export default Dialog;
//# sourceMappingURL=Dialog.js.map