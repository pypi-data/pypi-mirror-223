import { SessionManager } from '@jupyterlab/services';
import { UUID } from '@lumino/coreutils';
export class Kernel {
    _kernelManager;
    _kernelName;
    _kernelConnection;
    _session;
    _id;
    _info;
    constructor(props) {
        const { kernelManager, kernelName, kernelModel } = props;
        this._kernelManager = kernelManager;
        this._kernelName = kernelName;
        this._kernelConnection = this.requestJupyterKernel(kernelModel); // Request the effective Jupyter Kernel.
    }
    async requestJupyterKernel(kernelModel) {
        await this._kernelManager.ready;
        const sessionManager = new SessionManager({
            kernelManager: this._kernelManager,
            serverSettings: this._kernelManager.serverSettings,
            standby: 'never',
        });
        await sessionManager.ready;
        if (kernelModel) {
            console.log('Reusing a pre-existing kernel model.');
            const runningModel = sessionManager.running().next().value;
            this._session = sessionManager.connectTo({ model: runningModel });
        }
        else {
            const randomName = UUID.uuid4();
            this._session = await sessionManager.startNew({
                name: randomName,
                path: randomName,
                type: this._kernelName,
                kernel: {
                    name: this._kernelName,
                },
            });
        }
        this._info = await this._session.kernel.info;
        this._id = this._session.kernel.id;
        return this._session.kernel;
    }
    get id() {
        return this._id;
    }
    get info() {
        return this._info;
    }
    get session() {
        return this._session;
    }
    get connection() {
        return this._kernelConnection;
    }
    shutdown() {
        this._session.kernel?.shutdown();
        this.connection.then(k => k.dispose());
    }
}
export default Kernel;
//# sourceMappingURL=Kernel.js.map