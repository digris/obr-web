/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EmissionMedia } from './EmissionMedia';
import type { EmissionPlaylist } from './EmissionPlaylist';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Emission = {
    readonly url: string;
    readonly playlist: EmissionPlaylist;
    readonly ct: string;
    readonly uid: string;
    timeStart?: string | null;
    timeEnd?: string | null;
    readonly duration: string;
    mediaSet: Array<EmissionMedia>;
}
