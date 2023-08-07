import { NotebookModelFactory, NotebookModel } from "@jupyterlab/notebook";
export class JupyterReactNotebookModelFactory extends NotebookModelFactory {
    _nbformat;
    /** @override */
    constructor(options) {
        super(options);
        this._nbformat = options.nbformat;
    }
    /** @override */
    createNew(options) {
        if (this._nbformat) {
            const model = new NotebookModel();
            model.fromJSON(this._nbformat);
            return model;
        }
        return super.createNew(options);
    }
}
export default JupyterReactNotebookModelFactory;
//# sourceMappingURL=JupyterReactNotebookModelFactory.js.map