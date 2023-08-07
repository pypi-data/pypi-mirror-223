import { BoxPanel } from '@lumino/widgets';
import './CommandsAdapter.css';
declare class CommandsAdapter {
    private commandsPanel;
    constructor();
    get panel(): BoxPanel;
}
export default CommandsAdapter;
