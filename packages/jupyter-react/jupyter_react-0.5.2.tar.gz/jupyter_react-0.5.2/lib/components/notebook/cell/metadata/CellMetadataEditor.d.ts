import { Cell, ICellModel } from "@jupyterlab/cells";
type Props = {
    notebookId: string;
    cell: Cell<ICellModel>;
    nbgrader: boolean;
};
export declare const CellMetadataEditor: (props: Props) => import("react/jsx-runtime").JSX.Element;
export default CellMetadataEditor;
