import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import SettingsAdapter from './SettingsAdapter';
import Lumino from '../../jupyter/lumino/Lumino';
export const Settings = () => {
    const settingsAdapter = new SettingsAdapter();
    return _jsx(_Fragment, { children: _jsx(Lumino, { children: settingsAdapter.panel }) });
};
export default Settings;
//# sourceMappingURL=Settings.js.map