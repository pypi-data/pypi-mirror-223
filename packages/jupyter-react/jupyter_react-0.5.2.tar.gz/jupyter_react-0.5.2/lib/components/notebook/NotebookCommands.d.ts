import { CommandRegistry } from "@lumino/commands";
import { CompletionHandler } from "@jupyterlab/completer";
import { NotebookPanel } from '@jupyterlab/notebook';
/**
 * The map of command ids used by the notebook.
 */
export declare const cmdIds: {
    invoke: string;
    select: string;
    invokeNotebook: string;
    selectNotebook: string;
    startSearch: string;
    findNext: string;
    findPrevious: string;
    save: string;
    interrupt: string;
    restart: string;
    switchKernel: string;
    runAndAdvance: string;
    run: string;
    runAll: string;
    deleteCells: string;
    insertAbove: string;
    insertBelow: string;
    deleteCell: string;
    selectAbove: string;
    selectBelow: string;
    extendAbove: string;
    extendTop: string;
    extendBelow: string;
    extendBottom: string;
    editMode: string;
    merge: string;
    split: string;
    commandMode: string;
    undo: string;
    redo: string;
    changeCellType: string;
    toCode: string;
};
export declare const NotebookCommands: (commandRegistry: CommandRegistry, notebookPanel: NotebookPanel, completerHandler: CompletionHandler, path: string) => void;
export default NotebookCommands;
