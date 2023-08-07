import { MODULE_NAME, MODULE_VERSION } from "./Version";
/**
 * Activate the widget extension.
 */
export function activatePlotlyWidgetExtension(registry) {
    registry.registerWidget({
        name: MODULE_NAME,
        version: MODULE_VERSION,
        exports: () => import("./index"),
    });
}
//# sourceMappingURL=JupyterlabPlugin.js.map