import { BoxPanel } from '@lumino/widgets';
import { ITerminal } from '@jupyterlab/terminal';
import './TerminalAdapter.css';
export declare class TerminalAdapter {
    private terminalPanel;
    private terminal;
    constructor();
    get panel(): BoxPanel;
    setTheme(theme: ITerminal.Theme): void;
}
export default TerminalAdapter;
