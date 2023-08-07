import { Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { selectKernelStatus } from '../../components/notebook/NotebookState';
const NotebookToolbarStatus = (props) => {
    const { notebookId } = props;
    const kernelStatus = selectKernelStatus(notebookId);
    return (_jsxs(_Fragment, { children: ["Kernel Status: ", kernelStatus] }));
};
export default NotebookToolbarStatus;
//# sourceMappingURL=NotebookToolbarStatus.js.map