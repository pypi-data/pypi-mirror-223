import { ReactWidget } from '@jupyterlab/apputils';
import { IInputPrompt } from '@jupyterlab/cells';
/**
 * The custom input prompt implementation.
 */
export declare class InputPrompt extends ReactWidget implements IInputPrompt {
    private _executionCount;
    private state;
    constructor();
    /** @override */
    render(): import("react/jsx-runtime").JSX.Element;
    /**
     * The execution count for the prompt.
     */
    get executionCount(): string | null;
    set executionCount(value: string | null);
}
export default InputPrompt;
