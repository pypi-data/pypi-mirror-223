import { jsx as _jsx } from "react/jsx-runtime";
import FileBrowserAdapter from './FileBrowserAdapter';
import Lumino from '../../jupyter/lumino/Lumino';
export const FileBrowserLab = () => {
    const fileBrowserAdapter = new FileBrowserAdapter();
    return _jsx(Lumino, { children: fileBrowserAdapter.panel });
};
export default FileBrowserLab;
//# sourceMappingURL=FileBrowserLab.js.map