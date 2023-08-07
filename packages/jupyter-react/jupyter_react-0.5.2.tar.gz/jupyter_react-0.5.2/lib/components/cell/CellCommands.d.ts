import { CommandRegistry } from "@lumino/commands";
import { CompletionHandler } from "@jupyterlab/completer";
import { CodeCell } from '@jupyterlab/cells';
import { SessionContext } from '@jupyterlab/apputils';
export declare const CellCommands: (commandRegistry: CommandRegistry, codeCell: CodeCell, sessionContext: SessionContext, completerHandler: CompletionHandler) => void;
export default CellCommands;
