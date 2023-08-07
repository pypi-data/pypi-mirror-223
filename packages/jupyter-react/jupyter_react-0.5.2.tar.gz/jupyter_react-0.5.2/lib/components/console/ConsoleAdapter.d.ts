import { BoxPanel } from '@lumino/widgets';
import { ServiceManager } from '@jupyterlab/services';
declare class ConsoleAdapter {
    private _panel;
    constructor(serviceManager: ServiceManager);
    startConsole(path: string, serviceManager: ServiceManager.IManager, panel: BoxPanel): void;
    get panel(): BoxPanel;
}
export default ConsoleAdapter;
