import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel, INotebookTracker } from '@jupyterlab/notebook';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { ILoggerRegistry } from '@jupyterlab/logconsole';
import { DisposableDelegate } from '@lumino/disposable';
import { WidgetRenderer } from '@jupyter-widgets/jupyterlab-manager';
import * as base from '@jupyter-widgets/base';
export declare function registerWidgetManager(context: DocumentRegistry.IContext<INotebookModel>, rendermime: IRenderMimeRegistry, renderers: IterableIterator<WidgetRenderer>): DisposableDelegate;
/**
 * Activate the widget extension.
 */
export declare function activateWidgetExtension(rendermime: IRenderMimeRegistry, tracker: INotebookTracker | null, menu: IMainMenu | null, loggerRegistry: ILoggerRegistry | null): base.IJupyterWidgetRegistry;
