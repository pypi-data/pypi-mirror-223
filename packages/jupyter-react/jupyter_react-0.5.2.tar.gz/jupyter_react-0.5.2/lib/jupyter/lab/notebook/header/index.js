import { jsx as _jsx } from "react/jsx-runtime";
import { DisposableDelegate } from '@lumino/disposable';
import { ReactWidget } from '@jupyterlab/apputils';
import { ThemeProvider, BaseStyles, Text, Box } from '@primer/react';
class NotebookHeader extends ReactWidget {
    render() {
        return (_jsx(ThemeProvider, { children: _jsx(BaseStyles, { children: _jsx(Box, { children: _jsx(Text, { as: "p", sx: { color: 'fg.onEmphasis', bg: 'neutral.emphasis', p: 2, m: 0 }, children: "\uD83D\uDEA7 Datalayer Notebook" }) }) }) }));
    }
}
export class NotebookHeaderExtension {
    createNew(panel, _) {
        const notebookHeader = new NotebookHeader();
        notebookHeader.addClass('dla-Notebook-header');
        panel.contentHeader.insertWidget(0, notebookHeader);
        //    panel.content.model = null;
        return new DisposableDelegate(() => {
            notebookHeader.dispose();
        });
    }
}
//# sourceMappingURL=index.js.map