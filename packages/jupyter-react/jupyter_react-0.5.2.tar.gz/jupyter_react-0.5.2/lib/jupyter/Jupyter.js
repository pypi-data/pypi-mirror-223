import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { ThemeProvider, BaseStyles } from "@primer/react";
import { ErrorBoundary } from 'react-error-boundary';
import { JupyterContextProvider } from './JupyterContext';
import { getJupyterServerHttpUrl, getJupyterServerWsUrl, loadJupyterConfig } from './JupyterConfig';
import defaultInjectableStore from '../redux/Store';
import '@lumino/widgets/style/index.css';
import '@lumino/dragdrop/style/index.css';
import '@jupyterlab/ui-components/style/base.css';
import '@jupyterlab/apputils/style/base.css';
import '@jupyterlab/rendermime/style/base.css';
import '@jupyterlab/codeeditor/style/base.css';
import '@jupyterlab/documentsearch/style/base.css';
import '@jupyterlab/outputarea/style/base.css';
import '@jupyterlab/console/style/base.css';
import '@jupyterlab/completer/style/base.css';
import '@jupyterlab/codemirror/style/base.css';
import '@jupyterlab/codeeditor/style/base.css';
import '@jupyterlab/cells/style/base.css';
import '@jupyterlab/notebook/style/base.css';
import '@jupyterlab/filebrowser/style/base.css';
import '@jupyterlab/terminal/style/index.css';
import '@jupyterlab/theme-light-extension/style/theme.css';
import '@jupyterlab/theme-light-extension/style/variables.css';
import '@jupyter-widgets/base/css/index.css';
import '@jupyter-widgets/controls/css/widgets-base.css';
/**
 * The component to be used as fallback in case of error.
 */
const ErrorFallback = ({ error, resetErrorBoundary }) => {
    return (_jsxs("div", { role: "alert", children: [_jsx("p", { children: "Oops, something went wrong." }), _jsx("pre", { children: error.message }), _jsx("div", { style: { visibility: "hidden" }, children: _jsx("button", { onClick: resetErrorBoundary, children: "Try again" }) })] }));
};
/**
 * The Jupyter context. This handles the needed initialization
 * and ensure the Redux and the Material UI theme providers
 * are available.
 */
export const Jupyter = (props) => {
    const { lite, startDefaultKernel, defaultKernelName, injectableStore, useRunningKernelId, useRunningKernelIndex, children } = props;
    loadJupyterConfig(props);
    return (_jsx(ErrorBoundary, { FallbackComponent: ErrorFallback, onReset: () => { console.log('Error Boundary reset has been invoked...'); }, children: _jsx(ThemeProvider, { colorMode: "day", children: _jsx(BaseStyles, { children: _jsx(JupyterContextProvider, { lite: lite, startDefaultKernel: startDefaultKernel, defaultKernelName: defaultKernelName, useRunningKernelId: useRunningKernelId, useRunningKernelIndex: useRunningKernelIndex, baseUrl: getJupyterServerHttpUrl(), wsUrl: getJupyterServerWsUrl(), injectableStore: injectableStore || defaultInjectableStore, variant: "default", children: children }) }) }) }));
};
Jupyter.defaultProps = {
    lite: false,
    defaultKernelName: 'python',
    startDefaultKernel: true,
    collaborative: false,
    terminals: false,
    useRunningKernelIndex: -1,
};
export default Jupyter;
//# sourceMappingURL=Jupyter.js.map