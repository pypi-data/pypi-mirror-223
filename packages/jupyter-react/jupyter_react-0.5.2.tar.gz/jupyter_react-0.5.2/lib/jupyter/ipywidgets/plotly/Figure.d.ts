import { DOMWidgetModel, DOMWidgetView, ISerializers } from "@jupyter-widgets/base";
type InputDeviceState = {
    alt: any;
    ctrl: any;
    meta: any;
    shift: any;
    button: any;
    buttons: any;
};
type Points = {
    trace_indexes: number[];
    point_indexes: number[];
    xs: number[];
    ys: number[];
    zs?: number[];
};
type Selector = {
    type: "box" | "lasso";
    selector_state: {
        xrange: number[];
        yrange: number[];
    } | {
        xs: number[];
        ys: number[];
    };
};
/**
 * A FigureModel holds a mirror copy of the state of a FigureWidget on
 * the Python side.  There is a one-to-one relationship between JavaScript
 * FigureModels and Python FigureWidgets. The JavaScript FigureModel is
 * initialized as soon as a Python FigureWidget initialized, this happens
 * even before the widget is first displayed in the Notebook
 * @type {widgets.DOMWidgetModel}
 */
export declare class FigureModel extends DOMWidgetModel {
    defaults(): {
        _model_name: string;
        _model_module: any;
        _model_module_version: string;
        _view_name: string;
        _view_module: any;
        _view_module_version: string;
        _data: never[];
        _layout: {};
        _config: {};
        /**
         * @typedef {null|Object} Py2JsAddTracesMsg
         * @property {Array.<Object>} trace_data
         *  Array of traces to append to the end of the figure's current traces
         * @property {Number} trace_edit_id
         *  Edit ID to use when returning trace deltas using
         *  the _js2py_traceDeltas message.
         * @property {Number} layout_edit_id
         *  Edit ID to use when returning layout deltas using
         *  the _js2py_layoutDelta message.
         */
        _py2js_addTraces: null;
        /**
         * @typedef {null|Object} Py2JsDeleteTracesMsg
         * @property {Array.<Number>} delete_inds
         *  Array of indexes of traces to be deleted, in ascending order
         * @property {Number} trace_edit_id
         *  Edit ID to use when returning trace deltas using
         *  the _js2py_traceDeltas message.
         * @property {Number} layout_edit_id
         *  Edit ID to use when returning layout deltas using
         *  the _js2py_layoutDelta message.
         */
        _py2js_deleteTraces: null;
        /**
         * @typedef {null|Object} Py2JsMoveTracesMsg
         * @property {Array.<Number>} current_trace_inds
         *  Array of the current indexes of traces to be moved
         * @property {Array.<Number>} new_trace_inds
         *  Array of the new indexes that traces should be moved to.
         */
        _py2js_moveTraces: null;
        /**
         * @typedef {null|Object} Py2JsRestyleMsg
         * @property {Object} restyle_data
         *  Restyle data as accepted by Plotly.restyle
         * @property {null|Array.<Number>} restyle_traces
         *  Array of indexes of the traces that the resytle operation applies
         *  to, or null to apply the operation to all traces
         * @property {Number} trace_edit_id
         *  Edit ID to use when returning trace deltas using
         *  the _js2py_traceDeltas message
         * @property {Number} layout_edit_id
         *  Edit ID to use when returning layout deltas using
         *  the _js2py_layoutDelta message
         * @property {null|String} source_view_id
         *  view_id of the FigureView that triggered the original restyle
         *  event (e.g. by clicking the legend), or null if the restyle was
         *  triggered from Python
         */
        _py2js_restyle: null;
        /**
         * @typedef {null|Object} Py2JsRelayoutMsg
         * @property {Object} relayout_data
         *  Relayout data as accepted by Plotly.relayout
         * @property {Number} layout_edit_id
         *  Edit ID to use when returning layout deltas using
         *  the _js2py_layoutDelta message
         * @property {null|String} source_view_id
         *  view_id of the FigureView that triggered the original relayout
         *  event (e.g. by clicking the zoom button), or null if the
         *  relayout was triggered from Python
         */
        _py2js_relayout: null;
        /**
         * @typedef {null|Object} Py2JsUpdateMsg
         * @property {Object} style_data
         *  Style data as accepted by Plotly.update
         * @property {Object} layout_data
         *  Layout data as accepted by Plotly.update
         * @property {Array.<Number>} style_traces
         *  Array of indexes of the traces that the update operation applies
         *  to, or null to apply the operation to all traces
         * @property {Number} trace_edit_id
         *  Edit ID to use when returning trace deltas using
         *  the _js2py_traceDeltas message
         * @property {Number} layout_edit_id
         *  Edit ID to use when returning layout deltas using
         *  the _js2py_layoutDelta message
         * @property {null|String} source_view_id
         *  view_id of the FigureView that triggered the original update
         *  event (e.g. by clicking a button), or null if the update was
         *  triggered from Python
         */
        _py2js_update: null;
        /**
         * @typedef {null|Object} Py2JsAnimateMsg
         * @property {Object} style_data
         *  Style data as accepted by Plotly.animate
         * @property {Object} layout_data
         *  Layout data as accepted by Plotly.animate
         * @property {Array.<Number>} style_traces
         *  Array of indexes of the traces that the animate operation applies
         *  to, or null to apply the operation to all traces
         * @property {Object} animation_opts
         *  Animation options as accepted by Plotly.animate
         * @property {Number} trace_edit_id
         *  Edit ID to use when returning trace deltas using
         *  the _js2py_traceDeltas message
         * @property {Number} layout_edit_id
         *  Edit ID to use when returning layout deltas using
         *  the _js2py_layoutDelta message
         * @property {null|String} source_view_id
         *  view_id of the FigureView that triggered the original animate
         *  event (e.g. by clicking a button), or null if the update was
         *  triggered from Python
         */
        _py2js_animate: null;
        /**
         * @typedef {null|Object} Py2JsRemoveLayoutPropsMsg
         * @property {Array.<Array.<String|Number>>} remove_props
         *  Array of property paths to remove. Each propery path is an
         *  array of property names or array indexes that locate a property
         *  inside the _layout object
         */
        _py2js_removeLayoutProps: null;
        /**
         * @typedef {null|Object} Py2JsRemoveTracePropsMsg
         * @property {Number} remove_trace
         *  The index of the trace from which to remove properties
         * @property {Array.<Array.<String|Number>>} remove_props
         *  Array of property paths to remove. Each propery path is an
         *  array of property names or array indexes that locate a property
         *  inside the _data[remove_trace] object
         */
        _py2js_removeTraceProps: null;
        /**
         * @typedef {null|Object} Js2PyRestyleMsg
         * @property {Object} style_data
         *  Style data that was passed to Plotly.restyle
         * @property {Array.<Number>} style_traces
         *  Array of indexes of the traces that the restyle operation
         *  was applied to, or null if applied to all traces
         * @property {String} source_view_id
         *  view_id of the FigureView that triggered the original restyle
         *  event (e.g. by clicking the legend)
         */
        _js2py_restyle: null;
        /**
         * @typedef {null|Object} Js2PyRelayoutMsg
         * @property {Object} relayout_data
         *  Relayout data that was passed to Plotly.relayout
         * @property {String} source_view_id
         *  view_id of the FigureView that triggered the original relayout
         *  event (e.g. by clicking the zoom button)
         */
        _js2py_relayout: null;
        /**
         * @typedef {null|Object} Js2PyUpdateMsg
         * @property {Object} style_data
         *  Style data that was passed to Plotly.update
         * @property {Object} layout_data
         *  Layout data that was passed to Plotly.update
         * @property {Array.<Number>} style_traces
         *  Array of indexes of the traces that the update operation applied
         *  to, or null if applied to all traces
         * @property {String} source_view_id
         *  view_id of the FigureView that triggered the original relayout
         *  event (e.g. by clicking the zoom button)
         */
        _js2py_update: null;
        /**
         * @typedef {null|Object} Js2PyLayoutDeltaMsg
         * @property {Object} layout_delta
         *  The layout delta object that contains all of the properties of
         *  _fullLayout that are not identical to those in the
         *  FigureModel's _layout property
         * @property {Number} layout_edit_id
         *  Edit ID of message that triggered the creation of layout delta
         */
        _js2py_layoutDelta: null;
        /**
         * @typedef {null|Object} Js2PyTraceDeltasMsg
         * @property {Array.<Object>} trace_deltas
         *  Array of trace delta objects. Each trace delta contains the
         *  trace's uid along with all of the properties of _fullData that
         *  are not identical to those in the FigureModel's _data property
         * @property {Number} trace_edit_id
         *  Edit ID of message that triggered the creation of trace deltas
         */
        _js2py_traceDeltas: null;
        /**
         * Object representing a collection of points for use in click, hover,
         * and selection events
         * @typedef {Object} Points
         * @property {Array.<Number>} trace_indexes
         *  Array of the trace index for each point
         * @property {Array.<Number>} point_indexes
         *  Array of the index of each point in its own trace
         * @property {null|Array.<Number>} xs
         *  Array of the x coordinate of each point (for cartesian trace types)
         *  or null (for non-cartesian trace types)
         * @property {null|Array.<Number>} ys
         *  Array of the y coordinate of each point (for cartesian trace types)
         *  or null (for non-cartesian trace types
         * @property {null|Array.<Number>} zs
         *  Array of the z coordinate of each point (for 3D cartesian
         *  trace types)
         *  or null (for non-3D-cartesian trace types)
         */
        /**
         * Object representing the state of the input devices during a
         * plotly event
         * @typedef {Object} InputDeviceState
         * @property {boolean} alt - true if alt key pressed,
         * false otherwise
         * @property {boolean} ctrl - true if ctrl key pressed,
         * false otherwise
         * @property {boolean} meta - true if meta key pressed,
         * false otherwise
         * @property {boolean} shift - true if shift key pressed,
         * false otherwise
         *
         * @property {boolean} button
         *  Indicates which button was pressed on the mouse to trigger the
         *  event.
         *    0: Main button pressed, usually the left button or the
         *       un-initialized state
         *    1: Auxiliary button pressed, usually the wheel button or
         *       the middle button (if present)
         *    2: Secondary button pressed, usually the right button
         *    3: Fourth button, typically the Browser Back button
         *    4: Fifth button, typically the Browser Forward button
         *
         * @property {boolean} buttons
         *  Indicates which buttons were pressed on the mouse when the event
         *  is triggered.
         *    0  : No button or un-initialized
         *    1  : Primary button (usually left)
         *    2  : Secondary button (usually right)
         *    4  : Auxilary button (usually middle or mouse wheel button)
         *    8  : 4th button (typically the "Browser Back" button)
         *    16 : 5th button (typically the "Browser Forward" button)
         *
         *  Combinations of buttons are represented by the sum of the codes
         *  above. e.g. a value of 7 indicates buttons 1 (primary),
         *  2 (secondary), and 4 (auxilary) were pressed during the event
         */
        /**
         * @typedef {Object} BoxSelectorState
         * @property {Array.<Number>} xrange
         *  Two element array containing the x-range of the box selection
         * @property {Array.<Number>} yrange
         *  Two element array containing the y-range of the box selection
         */
        /**
         * @typedef {Object} LassoSelectorState
         * @property {Array.<Number>} xs
         *  Array of the x-coordinates of the lasso selection region
         * @property {Array.<Number>} ys
         *  Array of the y-coordinates of the lasso selection region
         */
        /**
         * Object representing the state of the selection tool during a
         * plotly_select event
         * @typedef {Object} Selector
         * @property {String} type
         *  Selection type. One of: 'box', or 'lasso'
         * @property {BoxSelectorState|LassoSelectorState} selector_state
         */
        /**
         * @typedef {null|Object} Js2PyPointsCallbackMsg
         * @property {string} event_type
         *  Name of the triggering event. One of 'plotly_click',
         *  'plotly_hover', 'plotly_unhover', or 'plotly_selected'
         * @property {null|Points} points
         *  Points object for event
         * @property {null|InputDeviceState} device_state
         *  InputDeviceState object for event
         * @property {null|Selector} selector
         *  State of the selection tool for 'plotly_selected' events, null
         *  for other event types
         */
        _js2py_pointsCallback: null;
        /**
         * @type {Number}
         * layout_edit_id of the last layout modification operation
         * requested by the Python side
         */
        _last_layout_edit_id: number;
        /**
         * @type {Number}
         * trace_edit_id of the last trace modification operation
         * requested by the Python side
         */
        _last_trace_edit_id: number;
    };
    /**
     * Initialize FigureModel. Called when the Python FigureWidget is first
     * constructed
     */
    initialize(): void;
    /**
     * Input a trace index specification and return an Array of trace
     * indexes where:
     *
     *  - null|undefined -> Array of all traces
     *  - Trace index as Number -> Single element array of input index
     *  - Array of trace indexes -> Input array unchanged
     *
     * @param {undefined|null|Number|Array.<Number>} trace_indexes
     * @returns {Array.<Number>}
     *  Array of trace indexes
     * @private
     */
    _normalize_trace_indexes(trace_indexes?: null | number | number[]): number[];
    /**
     * Log changes to the _data trait
     *
     * This should only happed on FigureModel initialization
     */
    do_data(): void;
    /**
     * Log changes to the _layout trait
     *
     * This should only happed on FigureModel initialization
     */
    do_layout(): void;
    /**
     * Handle addTraces message
     */
    do_addTraces(): void;
    /**
     * Handle deleteTraces message
     */
    do_deleteTraces(): void;
    /**
     * Handle moveTraces message
     */
    do_moveTraces(): void;
    /**
     * Handle restyle message
     */
    do_restyle(): void;
    /**
     * Handle relayout message
     */
    do_relayout(): void;
    /**
     * Handle update message
     */
    do_update(): void;
    /**
     * Handle animate message
     */
    do_animate(): void;
    /**
     * Handle removeLayoutProps message
     */
    do_removeLayoutProps(): void;
    /**
     * Handle removeTraceProps message
     */
    do_removeTraceProps(): void;
    static serializers: ISerializers;
    static model_name: string;
    static model_module: any;
    static model_module_version: string;
    static view_name: string;
    static view_module: any;
    static view_module_version: string;
}
/**
 * A FigureView manages the visual presentation of a single Plotly.js
 * figure for a single notebook output cell. Each FigureView has a
 * reference to FigureModel.  Multiple views may share a single model
 * instance, as is the case when a Python FigureWidget is displayed in
 * multiple notebook output cells.
 *
 * @type {widgets.DOMWidgetView}
 */
export declare class FigureView extends DOMWidgetView {
    viewID: string;
    /**
     * The perform_render method is called by processLuminoMessage
     * after the widget's DOM element has been attached to the notebook
     * output cell. This happens after the initialize of the
     * FigureModel, and it won't happen at all if the Python FigureWidget
     * is never displayed in a notebook output cell
     */
    perform_render(): void;
    /**
     * Respond to phosphorjs events
     */
    processLuminoMessage(msg: any): void;
    autosizeFigure(): void;
    /**
     * Purge Plotly.js data structures from the notebook output display
     * element when the view is destroyed
     */
    destroy(): void;
    /**
     * Return the figure's _fullData array merged with its data array
     *
     * The merge ensures that for any properties that el._fullData and
     * el.data have in common, we return the version from el.data
     *
     * Named colorscales are one example of why this is needed. The el.data
     * array will hold named colorscale strings (e.g. 'Viridis'), while the
     * el._fullData array will hold the actual colorscale array. e.g.
     *
     *      el.data[0].marker.colorscale == 'Viridis' but
     *      el._fullData[0].marker.colorscale = [[..., ...], ...]
     *
     * Performing the merge allows our FigureModel to retain the 'Viridis'
     * string, rather than having it overridded by the colorscale array.
     *
     */
    getFullData(): any;
    /**
     * Return the figure's _fullLayout object merged with its layout object
     *
     * See getFullData documentation for discussion of why the merge is
     * necessary
     */
    getFullLayout(): any;
    /**
     * Build Points data structure from data supplied by the plotly_click,
     * plotly_hover, or plotly_select events
     * @param {Object} data
     * @returns {null|Points}
     */
    buildPointsObject(data: any): null | Points;
    /**
     * Build InputDeviceState data structure from data supplied by the
     * plotly_click, plotly_hover, or plotly_select events
     * @param {Object} data
     * @returns {null|InputDeviceState}
     */
    buildInputDeviceStateObject(data: any): null | InputDeviceState;
    /**
     * Build Selector data structure from data supplied by the
     * plotly_select event
     * @param data
     * @returns {null|Selector}
     */
    buildSelectorObject(data: any): null | Selector;
    /**
     * Handle ploty_restyle events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_restyle(data: any): void;
    /**
     * Handle plotly_relayout events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_relayout(data: any): void;
    /**
     * Handle plotly_update events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_update(data: any): void;
    /**
     * Handle plotly_click events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_click(data: any): void;
    /**
     * Handle plotly_hover events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_hover(data: any): void;
    /**
     * Handle plotly_unhover events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_unhover(data: any): void;
    /**
     * Handle plotly_selected events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_selected(data: any): void;
    /**
     * Handle plotly_deselect events emitted by the Plotly.js library
     * @param data
     */
    handle_plotly_deselect(data: any): void;
    /**
     * Build and send a points callback message to the Python side
     *
     * @param {Object} data
     *  data object as provided by the plotly_click, plotly_hover,
     *  plotly_unhover, or plotly_selected events
     * @param {String} event_type
     *  Name of the triggering event. One of 'plotly_click',
     *  'plotly_hover', 'plotly_unhover', or 'plotly_selected'
     * @private
     */
    _send_points_callback_message(data: any, event_type: string): void;
    /**
     * Stub for future handling of plotly_doubleclick
     * @param data
     */
    handle_plotly_doubleclick(data: any): void;
    /**
     * Handle Plotly.addTraces request
     */
    do_addTraces(): void;
    /**
     * Handle Plotly.deleteTraces request
     */
    do_deleteTraces(): void;
    /**
     * Handle Plotly.moveTraces request
     */
    do_moveTraces(): void;
    /**
     * Handle Plotly.restyle request
     */
    do_restyle(): void;
    /**
     * Handle Plotly.relayout request
     */
    do_relayout(): void;
    /**
     * Handle Plotly.update request
     */
    do_update(): void;
    /**
     * Handle Plotly.animate request
     */
    do_animate(): void;
    /**
     * Construct layout delta object and send layoutDelta message to the
     * Python side
     *
     * @param layout_edit_id
     *  Edit ID of message that triggered the creation of the layout delta
     * @private
     */
    _sendLayoutDelta(layout_edit_id: any): void;
    /**
     * Construct trace deltas array for the requested trace indexes and
     * send traceDeltas message to the Python side
     *  Array of indexes of traces for which to compute deltas
     * @param trace_edit_id
     *  Edit ID of message that triggered the creation of trace deltas
     * @private
     */
    _sendTraceDeltas(trace_edit_id: any): void;
}
export {};
