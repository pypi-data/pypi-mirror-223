import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { createRoot } from 'react-dom/client';
import Jupyter from '../jupyter/Jupyter';
import { useJupyter } from '../jupyter/JupyterContext';
import Output from "../components/output/Output";
import "./../../style/index.css";
const SOURCE_1 = '1+1';
const SOURCE_1_OUTPUTS = [
    {
        "data": {
            "text/plain": [
                "2"
            ]
        },
        "execution_count": 1,
        "metadata": {},
        "output_type": "execute_result"
    }
];
const Outputs = () => {
    const { defaultKernel } = useJupyter();
    return (_jsx(_Fragment, { children: _jsx(Output, { showEditor: true, autoRun: false, kernel: defaultKernel, code: SOURCE_1, outputs: SOURCE_1_OUTPUTS }) }));
};
const div = document.createElement('div');
document.body.appendChild(div);
const root = createRoot(div);
root.render(_jsx(Jupyter, { lite: false, terminals: true, children: _jsx(Outputs, {}) }));
//# sourceMappingURL=Output.js.map