import { jsx as _jsx } from "react/jsx-runtime";
/**
 * The IPyWidgetsAttached class allows to render a Lumino
 * Widget being mounted in the React.js tree.
 */
const IPyWidgetsAttached = (props) => {
    const { Widget } = props;
    return _jsx("div", { ref: ref => {
            if (ref) {
                new Widget(ref);
            }
        } });
};
export default IPyWidgetsAttached;
//# sourceMappingURL=IPyWidgetsAttached.js.map