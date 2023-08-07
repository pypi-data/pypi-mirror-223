import React from 'react';
import { InjectableStore } from '../redux/Store';
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
 * Definition of the properties that can be passed
 * when creating a Jupyter context.
 */
export type JupyterProps = {
    children: React.ReactNode;
    lite: boolean;
    startDefaultKernel: boolean;
    defaultKernelName: string;
    useRunningKernelId?: string;
    useRunningKernelIndex?: number;
    injectableStore?: InjectableStore;
    collaborative?: boolean;
    jupyterServerHttpUrl?: string;
    jupyterServerWsUrl?: string;
    jupyterToken?: string;
    terminals?: boolean;
    theme?: any;
};
/**
 * The Jupyter context. This handles the needed initialization
 * and ensure the Redux and the Material UI theme providers
 * are available.
 */
export declare const Jupyter: {
    (props: JupyterProps): import("react/jsx-runtime").JSX.Element;
    defaultProps: {
        lite: boolean;
        defaultKernelName: string;
        startDefaultKernel: boolean;
        collaborative: boolean;
        terminals: boolean;
        useRunningKernelIndex: number;
    };
};
export default Jupyter;
