import { jsx as _jsx } from "react/jsx-runtime";
import { useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Widget } from '@lumino/widgets';
export const Lumino = (props) => {
    const ref = useRef(null);
    const { children } = props;
    useEffect(() => {
        const widget = children;
        try {
            Widget.attach(widget, ref.current);
        }
        catch (e) {
            console.warn('Exception while attaching Lumino widget.', e);
        }
        return () => {
            try {
                ReactDOM.unmountComponentAtNode(widget.node);
                widget.dispose();
                if (widget.isAttached || widget.node.isConnected) {
                    Widget.detach(widget);
                }
            }
            catch (e) {
                console.warn('Exception while detaching Lumino widget.', e);
            }
        };
    }, [children]);
    return _jsx("div", { ref: ref });
};
export default Lumino;
//# sourceMappingURL=Lumino.js.map