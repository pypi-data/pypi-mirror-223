import { Fragment as _Fragment, jsx as _jsx } from "react/jsx-runtime";
import { useState, useEffect, useRef } from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
/**
 * The class name added to InputPrompt.
 */
const INPUT_PROMPT_CLASS = 'jp-InputPrompt';
const Countdown = (props) => {
    const [count, setCount] = useState(props.count);
    let intervalRef = useRef();
    const decreaseNum = () => setCount((prev) => prev - 1);
    useEffect(() => {
        setCount(props.count);
    }, [props.count]);
    useEffect(() => {
        intervalRef.current = setInterval(decreaseNum, 1000);
        return () => clearInterval(intervalRef.current);
    }, []);
    return (_jsx(_Fragment, { children: count }));
};
/**
 * The custom input prompt implementation.
 */
export class InputPrompt extends ReactWidget {
    _executionCount = null;
    state = {
        count: 100
    };
    /*
    * Create an output prompt widget.
    */
    constructor() {
        super();
        this.addClass(INPUT_PROMPT_CLASS);
    }
    /** @override */
    render() {
        return _jsx(Countdown, { count: this.state.count });
    }
    /**
     * The execution count for the prompt.
     */
    get executionCount() {
        return this._executionCount;
    }
    set executionCount(value) {
        this._executionCount = value;
        if (value === null) {
            this.state = {
                count: 0
            };
        }
        else {
            if (value === '*') {
                this.state = {
                    count: 0
                };
            }
            else {
                this.state = {
                    count: Number(value)
                };
                this.update();
            }
        }
    }
}
export default InputPrompt;
//# sourceMappingURL=InputPrompt.js.map