import { Cell, ICellModel } from "@jupyterlab/cells";
export declare enum NbGraderType {
    NotGraded = 0,
    AutogradedAnswer = 1,
    AutogradedTest = 2,
    ManuallyGradedTask = 3,
    ManuallyGradedAnswer = 4,
    ReadonlyGraded = 5
}
export declare const getNbGraderType: (cell: Cell<ICellModel>) => NbGraderType;
export default NbGraderType;
