import { Dialog as JupyerLabDialog } from '@jupyterlab/apputils';
export class DialogAdapter {
    dialog;
    constructor() {
        this.dialog = new JupyerLabDialog({
            title: 'Dialog Title',
            body: 'This is the body of the dialog...',
            buttons: [
                JupyerLabDialog.cancelButton(),
                JupyerLabDialog.okButton(),
            ]
        });
    }
}
export default DialogAdapter;
//# sourceMappingURL=DialogAdapter.js.map