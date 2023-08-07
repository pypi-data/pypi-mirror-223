import { ISignal } from "@lumino/signaling";
import { Observable } from "rxjs";
/**
 * Convert a Lumino Signal to a rx-js Observable.
 */
export declare function asObservable<T>(signal: ISignal<unknown, T>): Observable<T>;
