import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { ActionList, TextInput } from "@primer/react";
import { CheckIcon } from "@primer/octicons-react";
import NbGraderType, { getNbGraderType } from './NbGraderCells';
export const CellMetadataEditor = (props) => {
    const { cell } = props;
    const [cellGradeType, setCellGradeType] = useState(getNbGraderType(cell));
    const [nbg, setNbg] = useState(cell.model.getMetadata('nbgrader') || { grade_id: '', points: 0 });
    const handleGradeIdChange = (cell, gradeId) => {
        const nbgrader = cell.model.getMetadata("nbgrader");
        cell.model.setMetadata("nbgrader", {
            ...nbgrader,
            grade_id: gradeId,
        });
        setNbg({
            ...nbg,
            grade_id: gradeId,
        });
    };
    const handlePointsChange = (cell, points) => {
        var points_number = +points;
        if (!isNaN(points_number)) {
            const nbgrader = cell.model.getMetadata("nbgrader");
            cell.model.setMetadata("nbgrader", {
                ...nbgrader,
                points: points_number,
            });
            setNbg({
                ...nbg,
                points: points_number,
            });
        }
    };
    const assignCellGradeType = (cell, cellGradeType) => {
        switch (cellGradeType) {
            case NbGraderType.NotGraded: {
                cell.model.deleteMetadata("nbgrader");
                setCellGradeType(NbGraderType.NotGraded);
                break;
            }
            case NbGraderType.AutogradedAnswer: {
                const nbgrader = cell.model.getMetadata("nbgrader");
                cell.model.setMetadata("nbgrader", {
                    ...nbgrader,
                    "grade": false,
                    "solution": true,
                    "locked": false,
                    "task": false,
                });
                setCellGradeType(NbGraderType.AutogradedAnswer);
                break;
            }
            case NbGraderType.AutogradedTest: {
                const nbgrader = cell.model.getMetadata("nbgrader");
                cell.model.setMetadata("nbgrader", {
                    ...nbgrader,
                    "grade": true,
                    "solution": false,
                    "locked": false,
                    "task": false,
                });
                setCellGradeType(NbGraderType.AutogradedTest);
                break;
            }
            case NbGraderType.ManuallyGradedAnswer: {
                const nbgrader = cell.model.getMetadata("nbgrader");
                cell.model.setMetadata("nbgrader", {
                    ...nbgrader,
                    "grade": true,
                    "solution": true,
                    "locked": false,
                    "task": false,
                });
                setCellGradeType(NbGraderType.ManuallyGradedAnswer);
                break;
            }
            case NbGraderType.ManuallyGradedTask: {
                const nbgrader = cell.model.getMetadata("nbgrader");
                cell.model.setMetadata("nbgrader", {
                    ...nbgrader,
                    //        "points": 1,
                    "grade": false,
                    "solution": false,
                    "locked": true,
                    "task": true,
                });
                setCellGradeType(NbGraderType.ManuallyGradedTask);
                break;
            }
            case NbGraderType.ReadonlyGraded: {
                const nbgrader = cell.model.getMetadata("nbgrader");
                cell.model.setMetadata("nbgrader", {
                    ...nbgrader,
                    "grade": false,
                    "solution": false,
                    "locked": true,
                    "task": false,
                });
                setCellGradeType(NbGraderType.ReadonlyGraded);
                break;
            }
        }
    };
    return (_jsxs(ActionList, { showDividers: true, children: [_jsx(ActionList.Divider, {}), _jsxs(ActionList.Group, { title: "NbGrader Cell Type", variant: "subtle", children: [_jsxs(ActionList.Item, { onSelect: e => assignCellGradeType(cell, NbGraderType.NotGraded), children: [cellGradeType === NbGraderType.NotGraded &&
                                _jsx(ActionList.LeadingVisual, { children: _jsx(CheckIcon, {}) }), "None", _jsx(ActionList.Description, { variant: "block", children: "Not a grader cell." })] }), _jsxs(ActionList.Item, { onSelect: e => assignCellGradeType(cell, NbGraderType.AutogradedAnswer), children: [cellGradeType === NbGraderType.AutogradedAnswer &&
                                _jsx(ActionList.LeadingVisual, { children: _jsx(CheckIcon, {}) }), "Autograded answer", _jsx(ActionList.Description, { variant: "block", children: "An autograded answer cell." })] }), _jsxs(ActionList.Item, { role: "listitem", onClick: e => assignCellGradeType(cell, NbGraderType.AutogradedTest), children: [cellGradeType === NbGraderType.AutogradedTest &&
                                _jsx(ActionList.LeadingVisual, { children: _jsx(CheckIcon, {}) }), "Autograded test", _jsx(ActionList.Description, { variant: "block", children: "An autograded test cell." })] }), _jsxs(ActionList.Item, { onSelect: e => assignCellGradeType(cell, NbGraderType.ManuallyGradedTask), children: [cellGradeType === NbGraderType.ManuallyGradedTask &&
                                _jsx(ActionList.LeadingVisual, { children: _jsx(CheckIcon, {}) }), "Manually graded task", _jsx(ActionList.Description, { variant: "block", children: "A manually graded task cell." })] }), _jsxs(ActionList.Item, { onSelect: e => assignCellGradeType(cell, NbGraderType.ManuallyGradedAnswer), children: [cellGradeType === NbGraderType.ManuallyGradedAnswer &&
                                _jsx(ActionList.LeadingVisual, { children: _jsx(CheckIcon, {}) }), "Manually graded answer", _jsx(ActionList.Description, { variant: "block", children: "A manually graded answer cell." })] }), _jsxs(ActionList.Item, { onSelect: e => assignCellGradeType(cell, NbGraderType.ReadonlyGraded), children: [cellGradeType === NbGraderType.ReadonlyGraded &&
                                _jsx(ActionList.LeadingVisual, { children: _jsx(CheckIcon, {}) }), "Readonly", _jsx(ActionList.Description, { variant: "block", children: "A readonly grader cell." })] })] }), cellGradeType !== NbGraderType.NotGraded &&
                _jsxs(ActionList.Group, { title: "NbGrader Metadata", variant: "subtle", children: [_jsxs(ActionList.Item, { onSelect: e => e.preventDefault(), children: ["Grade ID: ", _jsx(TextInput, { block: true, value: nbg.grade_id, onChange: e => { e.preventDefault(); handleGradeIdChange(cell, e.target.value); } })] }), _jsxs(ActionList.Item, { children: ["Points: ", _jsx(TextInput, { block: true, value: nbg.points, onChange: e => { e.preventDefault(); handlePointsChange(cell, e.target.value); } })] })] })] }));
};
export default CellMetadataEditor;
//# sourceMappingURL=CellMetadataEditor.js.map