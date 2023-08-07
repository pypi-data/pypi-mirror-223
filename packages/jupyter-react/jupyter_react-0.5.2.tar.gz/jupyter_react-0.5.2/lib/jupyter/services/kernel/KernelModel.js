import { Signal } from '@lumino/signaling';
export class KernelModel {
    constructor(session) {
        this._sessionContext = session;
    }
    get future() {
        return this._future;
    }
    set future(value) {
        this._future = value;
        if (!value) {
            return;
        }
        value.onIOPub = this._onIOPub;
    }
    get output() {
        return this._output;
    }
    get stateChanged() {
        return this._stateChanged;
    }
    execute(code) {
        if (!this._sessionContext || !this._sessionContext.session?.kernel) {
            return;
        }
        this.future = this._sessionContext.session?.kernel?.requestExecute({
            code
        });
    }
    _onIOPub = (msg) => {
        const msgType = msg.header.msg_type;
        switch (msgType) {
            case 'execute_result':
                break;
            case 'display_data':
                break;
            case 'update_display_data':
                this._output = msg.content;
                this._stateChanged.emit();
                break;
            default:
                break;
        }
        return;
    };
    _future = null;
    _output = null;
    _sessionContext;
    _stateChanged = new Signal(this);
}
export default KernelModel;
//# sourceMappingURL=KernelModel.js.map