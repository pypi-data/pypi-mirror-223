import { jsx as _jsx } from "react/jsx-runtime";
import { ReactWidget } from '@jupyterlab/apputils';
import JupyterReact from '../../app/JupyterReact';
export class JupyterReactWidget extends ReactWidget {
    constructor() {
        super();
        this.addClass('dla-Container');
    }
    render() {
        return _jsx(JupyterReact, {});
    }
}
//# sourceMappingURL=widget.js.map