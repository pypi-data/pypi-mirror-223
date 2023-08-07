import { OutputArea, OutputAreaModel } from '@jupyterlab/outputarea';
import { RenderMimeRegistry, standardRendererFactories } from '@jupyterlab/rendermime';
import { rendererFactory as jsonRendererFactory } from '@jupyterlab/json-extension';
import { rendererFactory as javascriptRendererFactory } from '@jupyterlab/javascript-extension';
import { requireLoader } from "@jupyter-widgets/html-manager";
import { WIDGET_MIMETYPE, WidgetRenderer } from "@jupyter-widgets/html-manager/lib/output_renderers";
import { IPyWidgetsClassicManager } from "../../jupyter/ipywidgets/IPyWidgetsClassicManager";
// import { activateWidgetExtension } from "./../../jupyter/ipywidgets/IPyWidgetsJupyterLabPlugin";
// import { activatePlotlyWidgetExtension } from "./../../jupyter/ipywidgets/plotly/JupyterlabPlugin";
export class OutputAdapter {
    _kernel;
    _renderers;
    _outputArea;
    _rendermime;
    _iPyWidgetsClassicManager;
    constructor(kernel, outputs) {
        this._kernel = kernel;
        this._renderers = standardRendererFactories.filter(factory => factory.mimeTypes[0] !== 'text/javascript');
        this._renderers.push(jsonRendererFactory);
        this._renderers.push(javascriptRendererFactory);
        this._rendermime = new RenderMimeRegistry({
            initialFactories: this._renderers,
        });
        this._iPyWidgetsClassicManager = new IPyWidgetsClassicManager({ loader: requireLoader });
        this._rendermime.addFactory({
            safe: false,
            mimeTypes: [WIDGET_MIMETYPE],
            createRenderer: (options) => new WidgetRenderer(options, this._iPyWidgetsClassicManager),
        }, 0);
        //    const widgetRegistry = activateWidgetExtension(this._rendermime, null, null, null);
        //    activatePlotlyWidgetExtension(widgetRegistry);
        const outputAreaModel = new OutputAreaModel({
            trusted: true,
            values: outputs,
        });
        this._outputArea = new OutputArea({
            model: outputAreaModel,
            rendermime: this._rendermime,
        });
        this.initKernel();
    }
    execute(code) {
        if (this._kernel) {
            this.clearOutput();
            this._kernel.connection.then((kernelConnection) => {
                this._outputArea.future = kernelConnection.requestExecute({ code });
            });
        }
    }
    interrupt() {
        if (this._kernel) {
            this._kernel.connection.then((kernelConnection) => {
                kernelConnection.interrupt();
            });
        }
    }
    clearOutput() {
        this._outputArea.model.clear();
    }
    get kernel() {
        return this._kernel;
    }
    set kernel(kernel) {
        this._kernel = kernel;
        this.initKernel();
    }
    get outputArea() {
        return this._outputArea;
    }
    initKernel() {
        if (this._kernel) {
            this._kernel.connection.then((kernelConnection) => {
                this._iPyWidgetsClassicManager.registerWithKernel(kernelConnection);
            });
        }
    }
}
export default OutputAdapter;
//# sourceMappingURL=OutputAdapter.js.map