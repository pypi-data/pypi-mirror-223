import { Observable } from "rxjs";
/**
 * Convert a Lumino Signal to a rx-js Observable.
 */
export function asObservable(signal) {
    return new Observable((subscriber) => {
        function slot(_, args) {
            subscriber.next(args);
        }
        signal.connect(slot);
        return () => {
            signal.disconnect(slot);
        };
    });
}
//# sourceMappingURL=LuminoObservable.js.map