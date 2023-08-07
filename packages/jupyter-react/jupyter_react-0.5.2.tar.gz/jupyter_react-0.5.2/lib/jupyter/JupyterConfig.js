import { PageConfig } from '@jupyterlab/coreutils';
/**
 * The default Jupyter configuration.
 */
let config = {
    jupyterServerHttpUrl: '',
    jupyterServerWsUrl: '',
    jupyterToken: '',
};
/**
 * Setter for jupyterServerHttpUrl.
 */
export const setJupyterServerHttpUrl = (jupyterServerHttpUrl) => {
    config.jupyterServerHttpUrl = jupyterServerHttpUrl;
};
/**
 * Getter for jupyterServerHttpUrl.
 */
export const getJupyterServerHttpUrl = () => config.jupyterServerHttpUrl;
/**
 * Setter for jupyterServerWsUrl.
 */
export const setJupyterServerWsUrl = (jupyterServerWsUrl) => {
    config.jupyterServerWsUrl = jupyterServerWsUrl;
};
/**
 * Getter for jupyterServerWsUrl.
 */
export const getJupyterServerWsUrl = () => config.jupyterServerWsUrl;
/**
 * Setter for jupyterToken.
 */
export const setJupyterToken = (jupyterToken) => {
    config.jupyterToken = jupyterToken;
};
/**
 * Getter for jupyterToken.
 */
export const getJupyterToken = () => config.jupyterToken;
/**
 * Method to load the Jupyter configuration from the
 * host HTML page.
 */
export const loadJupyterConfig = (props) => {
    const { lite, jupyterServerHttpUrl, jupyterServerWsUrl, collaborative, terminals, jupyterToken } = props;
    const htmlConfig = document.getElementById('datalayer-config-data');
    if (htmlConfig) {
        config = JSON.parse(htmlConfig.textContent || '');
    }
    if (lite) {
        setJupyterServerHttpUrl(location.protocol + '//' + location.host);
    }
    else if (config.jupyterServerHttpUrl) {
        setJupyterServerHttpUrl(config.jupyterServerHttpUrl);
    }
    else {
        setJupyterServerHttpUrl(jupyterServerHttpUrl || location.protocol + '//' + location.host + "/api/jupyter");
    }
    if (lite) {
        setJupyterServerWsUrl(location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host);
    }
    else if (config.jupyterServerWsUrl) {
        setJupyterServerWsUrl(config.jupyterServerWsUrl);
    }
    else {
        setJupyterServerWsUrl(jupyterServerWsUrl || location.protocol.replace('http', 'ws') + '//' + location.host + "/api/jupyter");
    }
    if (config.jupyterToken) {
        setJupyterToken(config.jupyterToken);
    }
    else {
        setJupyterToken(jupyterToken || '');
    }
    PageConfig.setOption('baseUrl', getJupyterServerHttpUrl());
    PageConfig.setOption('wsUrl', getJupyterServerWsUrl());
    PageConfig.setOption('token', getJupyterToken());
    PageConfig.setOption('collaborative', String(collaborative || false));
    PageConfig.setOption('terminalsAvailable', String(terminals || false));
    PageConfig.setOption('mathjaxUrl', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js');
    PageConfig.setOption('mathjaxConfig', 'TeX-AMS_CHTML-full,Safe');
    return config;
};
//# sourceMappingURL=JupyterConfig.js.map