import { HTMLManager } from "@jupyter-widgets/html-manager";
import { shims } from "@jupyter-widgets/base/lib/services-shim";
import * as luminoWidget from "@lumino/widgets";
import * as outputWidgets from "@jupyter-widgets/jupyterlab-manager/lib/output";
// Exposing @jupyter-widgets/base and @jupyter-widgets/controls as AMD modules for custom widget bundles that depend on it.
import * as base from "@jupyter-widgets/base";
import * as controls from "@jupyter-widgets/controls";
if (typeof window !== "undefined" && typeof window.define !== "undefined") {
    window.define("@jupyter-widgets/base", base);
    window.define("@jupyter-widgets/controls", controls);
}
/**
 * The class responsible for the classic IPyWidget rendering.
 */
export class IPyWidgetsClassicManager extends HTMLManager {
    _kernelConnection;
    _commRegistration;
    _onError;
    registerWithKernel(kernelConnection) {
        this._kernelConnection = kernelConnection;
        if (this._commRegistration) {
            this._commRegistration.dispose();
        }
        if (kernelConnection) {
            this._commRegistration = kernelConnection.registerCommTarget(this.comm_target_name, (comm, message) => {
                this.handle_comm_open(new shims.services.Comm(comm), message);
            });
        }
    }
    get onError() {
        return this._onError;
    }
    display_view(view, el) {
        return Promise.resolve(view).then((view) => {
            luminoWidget.Widget.attach(view.luminoWidget, el);
            view.on("remove", function () {
                console.log("view removed", view);
            });
            //      return view;
        });
    }
    loadClass(className, moduleName, moduleVersion) {
        if (moduleName === "@jupyter-widgets/output") {
            return Promise.resolve(outputWidgets).then((module) => {
                if (module[className]) {
                    return module[className];
                }
                else {
                    return Promise.reject(`Class ${className} not found in module ${moduleName}`);
                }
            });
        }
        else {
            return super.loadClass(className, moduleName, moduleVersion);
        }
    }
    callbacks(view) {
        const baseCallbacks = super.callbacks(view);
        return Object.assign({}, baseCallbacks, {
            iopub: { output: (msg) => this._onError.emit(msg) },
        });
    }
    _create_comm(target_name, model_id, data, metadata, buffers) {
        const comm = this._kernelConnection?.createComm(target_name, model_id);
        if (data || metadata) {
            comm?.open(data, metadata);
        }
        return Promise.resolve(new shims.services.Comm(comm));
    }
    _get_comm_info() {
        return this._kernelConnection
            .requestCommInfo({ target_name: this.comm_target_name })
            .then((reply) => reply.content.comms);
    }
}
//# sourceMappingURL=IPyWidgetsClassicManager.js.map