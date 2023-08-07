import { DockPanel } from '@lumino/widgets';
import './SettingsAdapter.css';
declare class SettingsAdapter {
    private settingsPanel;
    constructor();
    get panel(): DockPanel;
}
export default SettingsAdapter;
