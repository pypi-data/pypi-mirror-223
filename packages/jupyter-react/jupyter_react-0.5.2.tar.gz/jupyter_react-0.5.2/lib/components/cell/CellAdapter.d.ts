import { BoxPanel } from '@lumino/widgets';
import { SessionContext } from '@jupyterlab/apputils';
import { CodeCell } from '@jupyterlab/cells';
import { ServerConnection } from '@jupyterlab/services';
import Kernel from './../../jupyter/services/kernel/Kernel';
export declare class CellAdapter {
    private _panel;
    private _codeCell;
    private _sessionContext;
    constructor(source: string, serverSettings: ServerConnection.ISettings, kernel?: Kernel);
    get panel(): BoxPanel;
    get codeCell(): CodeCell;
    get sessionContext(): SessionContext;
    execute: () => void;
}
export default CellAdapter;
