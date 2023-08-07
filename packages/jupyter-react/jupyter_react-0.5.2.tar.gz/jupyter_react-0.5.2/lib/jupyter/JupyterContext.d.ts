import React from "react";
import { ServiceManager, ServerConnection, KernelManager } from '@jupyterlab/services';
import { InjectableStore } from './../redux/Store';
import Kernel from './services/kernel/Kernel';
/**
 * The type for the Jupyter context.
 */
export type JupyterContextType = {
    lite: boolean;
    serverSettings: ServerConnection.ISettings;
    serviceManager?: ServiceManager;
    kernelManager?: KernelManager;
    defaultKernel?: Kernel;
    startDefaultKernel: boolean;
    variant: string;
    setVariant: (value: string) => void;
    baseUrl: string;
    wsUrl: string;
    injectableStore: InjectableStore;
};
/**
 * The instance for the Jupyter context.
 */
export declare const JupyterContext: React.Context<JupyterContextType | undefined>;
export declare const useJupyter: () => JupyterContextType;
/**
 * The type for the Jupyter context consumer.
 */
export declare const JupyterContextConsumer: React.Consumer<JupyterContextType | undefined>;
/**
 * Utiliy method to ensure the Jupyter context is authenticated
 * with the Jupyter server.
 */
export declare const ensureJupyterAuth: (serverSettings: ServerConnection.ISettings) => Promise<boolean>;
export declare const createServerSettings: (baseUrl: string, wsUrl: string) => ServerConnection.ISettings;
/**
 * The Jupyter context provider.
 */
export declare const JupyterContextProvider: React.FC<{
    children: React.ReactNode;
    lite: boolean;
    startDefaultKernel: boolean;
    defaultKernelName: string;
    useRunningKernelId?: string;
    useRunningKernelIndex?: number;
    variant: string;
    baseUrl: string;
    wsUrl: string;
    injectableStore: InjectableStore;
}>;
