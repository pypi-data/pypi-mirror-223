import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect, useReducer } from 'react';
import { TreeView } from '@primer/react';
import { FileIcon } from '@primer/octicons-react';
import { useJupyter } from './../../jupyter/JupyterContext';
import Services from './../../jupyter/services/Services';
const initialTree = {
    id: 'root',
    name: 'Jupyter Content',
};
export const FileBrowser = () => {
    const [tree, setTree] = useState(initialTree);
    const [, forceUpdate] = useReducer(x => x + 1, 0);
    const { serviceManager } = useJupyter();
    const loadPath = (services, subTree, path) => {
        const loadFolderItems = (services, path) => {
            const folderItems = services
                .contents()
                .get(path.join('/'))
                .then(res => {
                const items = res.content.map((e) => {
                    if (e.type === 'directory') {
                        return {
                            id: 'folder_' + e.name,
                            name: e.name,
                            children: new Array(),
                        };
                    }
                    else {
                        return {
                            id: 'file_' + e.name,
                            name: e.name,
                        };
                    }
                });
                return items;
            });
            return folderItems;
        };
        loadFolderItems(services, path).then(folderItems => {
            subTree.children = folderItems;
            for (const child of subTree.children) {
                if (child.id.startsWith('folder_')) {
                    loadPath(services, child, path.concat(child.name));
                }
            }
            setTree(initialTree);
            forceUpdate();
        });
    };
    useEffect(() => {
        if (serviceManager) {
            const services = new Services(serviceManager);
            loadPath(services, initialTree, []);
        }
    }, [serviceManager]);
    const renderTree = (nodes) => {
        return nodes.map((node) => (_jsxs(TreeView.Item, { id: node.id, children: [_jsx(TreeView.LeadingVisual, { children: Array.isArray(node.children) ? (_jsx(TreeView.DirectoryIcon, {})) : (_jsx(FileIcon, {})) }), node.name, Array.isArray(node.children) && (_jsx(TreeView.SubTree, { children: renderTree(node.children) }))] })));
    };
    return (_jsx(_Fragment, { children: _jsx(TreeView, { children: _jsxs(TreeView.Item, { id: tree.id, defaultExpanded: true, children: [_jsx(TreeView.LeadingVisual, { children: _jsx(TreeView.DirectoryIcon, {}) }), tree.name, Array.isArray(tree.children) && (_jsx(TreeView.SubTree, { children: renderTree(tree.children) }))] }) }) }));
};
export default FileBrowser;
//# sourceMappingURL=FileBrowser.js.map