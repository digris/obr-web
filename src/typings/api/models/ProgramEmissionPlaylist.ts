/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlaylistImage } from './PlaylistImage';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type ProgramEmissionPlaylist = {
    /**
     * Content type
     */
    readonly ct: string;
    /**
     * UID
     */
    readonly uid: string;
    readonly url: string;
    name?: string;
    readonly image: PlaylistImage | null;
};

