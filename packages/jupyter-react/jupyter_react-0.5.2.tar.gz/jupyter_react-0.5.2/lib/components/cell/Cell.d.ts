export type ICellProps = {
    source?: string;
    autoStart?: boolean;
};
export declare const Cell: {
    (props: ICellProps): import("react/jsx-runtime").JSX.Element;
    defaultProps: Partial<ICellProps>;
};
export default Cell;
