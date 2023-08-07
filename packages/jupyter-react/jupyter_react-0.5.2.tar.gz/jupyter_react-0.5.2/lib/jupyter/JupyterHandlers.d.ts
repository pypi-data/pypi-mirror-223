import { ServerConnection } from '@jupyterlab/services';
/**
 * Call the Jupyter server API.
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
export declare function requestAPI<T>(serverSettings: ServerConnection.ISettings, namespace?: string, endPoint?: string, init?: RequestInit): Promise<T>;
