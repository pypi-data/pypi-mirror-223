import { Widget } from '@lumino/widgets';
import { ManagerBase } from '@jupyter-widgets/base-manager';
import * as base from '@jupyter-widgets/base';
import * as controls from '@jupyter-widgets/controls';
export class IPyWidgetsManager extends ManagerBase {
    el;
    constructor(el) {
        super();
        this.el = el;
    }
    async loadClass(className, moduleName, moduleVersion) {
        return new Promise(function (resolve, reject) {
            if (moduleName === '@jupyter-widgets/controls') {
                resolve(controls);
            }
            else if (moduleName === '@jupyter-widgets/base') {
                resolve(base);
            }
            else {
                var fallback = function (err) {
                    let failedId = err.requireModules && err.requireModules[0];
                    if (failedId) {
                        console.log(`Falling back to jsDelivr for ${moduleName}@${moduleVersion}`);
                        window.require([
                            `https://cdn.jsdelivr.net/npm/${moduleName}@${moduleVersion}/dist/index.js`,
                        ], resolve, reject);
                    }
                    else {
                        throw err;
                    }
                };
                window.require([`${moduleName}.js`], resolve, fallback);
            }
        }).then(function (module) {
            if (module[className]) {
                return module[className];
            }
            else {
                return Promise.reject(`Class ${className} not found in module ${moduleName}@${moduleVersion}`);
            }
        });
    }
    async display_view(view) {
        var that = this;
        return Promise.resolve(view).then(function (view) {
            Widget.attach(view.luminoWidget, that.el);
            return view;
        });
    }
    _get_comm_info() {
        return Promise.resolve({});
    }
    _create_comm() {
        return Promise.reject('no comms available');
    }
}
export default IPyWidgetsManager;
//# sourceMappingURL=IPyWidgetsManager.js.map