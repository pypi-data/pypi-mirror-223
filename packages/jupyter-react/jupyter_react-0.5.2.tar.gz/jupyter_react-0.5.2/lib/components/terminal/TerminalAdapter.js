import { BoxPanel } from '@lumino/widgets';
import { TerminalManager } from '@jupyterlab/services';
import { Terminal } from '@jupyterlab/terminal';
import './TerminalAdapter.css';
export class TerminalAdapter {
    terminalPanel;
    terminal;
    constructor() {
        this.terminalPanel = new BoxPanel();
        this.terminalPanel.addClass('dla-JupyterLab-terminal');
        this.terminalPanel.spacing = 0;
        const manager = new TerminalManager();
        manager.startNew().then((terminalConnection) => {
            this.terminal = new Terminal(terminalConnection, { theme: 'light' });
            this.terminal.title.closable = true;
            this.terminalPanel.addWidget(this.terminal);
        });
    }
    get panel() {
        return this.terminalPanel;
    }
    setTheme(theme) {
        this.terminal.setOption('theme', theme);
    }
}
export default TerminalAdapter;
//# sourceMappingURL=TerminalAdapter.js.map