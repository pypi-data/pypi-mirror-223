import { SplitPanel } from '@lumino/widgets';
import './FileBrowserAdapter.css';
declare class FileBrowserAdapter {
    private fileBrowserPanel;
    constructor();
    get panel(): SplitPanel;
}
export default FileBrowserAdapter;
