import { jsx as _jsx } from "react/jsx-runtime";
import { useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Widget } from '@lumino/widgets';
export const LuminoNotebook = (props) => {
    const { adapter } = props;
    const panel = adapter.panel;
    const ref = useRef(null);
    useEffect(() => {
        if (!panel) {
            return;
        }
        Widget.attach(panel, ref.current);
        return () => {
            try {
                ReactDOM.unmountComponentAtNode(panel.node);
                if (panel.isAttached) {
                    Widget.detach(panel);
                }
                adapter.dispose();
            }
            catch (e) {
                console.warn('Exception while detaching Lumino widget.', e);
            }
        };
    }, [adapter.uid]);
    return _jsx("div", { ref: ref });
};
export default LuminoNotebook;
//# sourceMappingURL=LuminoNotebook.js.map