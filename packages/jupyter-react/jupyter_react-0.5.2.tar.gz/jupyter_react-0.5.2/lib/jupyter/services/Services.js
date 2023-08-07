export class Services {
    _serviceManager;
    constructor(services) {
        this._serviceManager = services;
    }
    kernelspecs() {
        return this._serviceManager.kernelspecs;
    }
    contents() {
        return this._serviceManager.contents;
    }
    nbconvert() {
        return this._serviceManager.nbconvert;
    }
    sessions() {
        return this._serviceManager.sessions;
    }
    settings() {
        return this._serviceManager.settings;
    }
    terminals() {
        return this._serviceManager.terminals;
    }
    workspaces() {
        return this._serviceManager.workspaces;
    }
    builder() {
        return this._serviceManager.builder;
    }
    serverSettings() {
        return this._serviceManager.serverSettings;
    }
    refreshKernelspecs() {
        return this.kernelspecs().refreshSpecs();
    }
    getKernelspecs() {
        return this.kernelspecs().specs;
    }
}
export default Services;
//# sourceMappingURL=Services.js.map