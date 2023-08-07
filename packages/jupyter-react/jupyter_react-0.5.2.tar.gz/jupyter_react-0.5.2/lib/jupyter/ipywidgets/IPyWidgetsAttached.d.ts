/**
 * The IPyWidgetsAttached class allows to render a Lumino
 * Widget being mounted in the React.js tree.
 */
declare const IPyWidgetsAttached: (props: {
    Widget: any;
}) => import("react/jsx-runtime").JSX.Element;
export default IPyWidgetsAttached;
