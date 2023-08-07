import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import IPyWidgetsAttached from '../../jupyter/ipywidgets/IPyWidgetsAttached';
import './IPyWidgetsComponent.css';
export const IPyWidgetsComponent = (props) => {
    const { Widget } = props;
    return _jsx(_Fragment, { children: _jsx(IPyWidgetsAttached, { Widget: Widget }) });
};
export default IPyWidgetsComponent;
//# sourceMappingURL=IPyWidgetsComponent.js.map