/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EmissionMediaSet } from './EmissionMediaSet';
import type { EmissionPlaylist } from './EmissionPlaylist';
import type { EmissionVote } from './EmissionVote';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Emission = {
    /**
     * Content type
     */
    readonly ct: string;
    /**
     * UID
     */
    readonly uid: string;
    readonly url: string;
    readonly playlist: EmissionPlaylist;
    timeStart?: string | null;
    timeEnd?: string | null;
    readonly duration: string;
    readonly liveRatings: Array<EmissionVote>;
    readonly mediaSet: Array<EmissionMediaSet>;
};

