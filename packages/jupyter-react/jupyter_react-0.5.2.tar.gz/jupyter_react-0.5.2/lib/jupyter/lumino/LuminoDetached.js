import { jsx as _jsx } from "react/jsx-runtime";
import React from 'react';
/**
 * The LuminoDetached class allows to render a Lumino
 * Widget that is not mounted in the React.js tree.
 */
export class LuminoDetached extends React.Component {
    render() {
        return _jsx("div", { ref: ref => { } });
    }
}
export default LuminoDetached;
//# sourceMappingURL=LuminoDetached.js.map