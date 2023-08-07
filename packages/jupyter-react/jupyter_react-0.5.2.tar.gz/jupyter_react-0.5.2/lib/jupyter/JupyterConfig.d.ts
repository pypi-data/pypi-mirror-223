import { JupyterProps } from './Jupyter';
/**
 * Type of the Jupyter configuration.
 */
export type IJupyterConfig = {
    jupyterServerHttpUrl: string;
    jupyterServerWsUrl: string;
    jupyterToken: string;
};
/**
 * Setter for jupyterServerHttpUrl.
 */
export declare const setJupyterServerHttpUrl: (jupyterServerHttpUrl: string) => void;
/**
 * Getter for jupyterServerHttpUrl.
 */
export declare const getJupyterServerHttpUrl: () => string;
/**
 * Setter for jupyterServerWsUrl.
 */
export declare const setJupyterServerWsUrl: (jupyterServerWsUrl: string) => void;
/**
 * Getter for jupyterServerWsUrl.
 */
export declare const getJupyterServerWsUrl: () => string;
/**
 * Setter for jupyterToken.
 */
export declare const setJupyterToken: (jupyterToken: string) => void;
/**
 * Getter for jupyterToken.
 */
export declare const getJupyterToken: () => string;
/**
 * Method to load the Jupyter configuration from the
 * host HTML page.
 */
export declare const loadJupyterConfig: (props: JupyterProps) => IJupyterConfig;
