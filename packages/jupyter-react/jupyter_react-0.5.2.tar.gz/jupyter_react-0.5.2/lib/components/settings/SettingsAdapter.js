import { DockPanel } from '@lumino/widgets';
import './SettingsAdapter.css';
class SettingsAdapter {
    settingsPanel;
    constructor() {
        this.settingsPanel = new DockPanel();
        this.settingsPanel.id = 'dla-jlab-settings';
        this.settingsPanel.spacing = 0;
    }
    get panel() {
        return this.settingsPanel;
    }
}
export default SettingsAdapter;
//# sourceMappingURL=SettingsAdapter.js.map