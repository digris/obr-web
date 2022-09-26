/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MediaArtist } from './MediaArtist';
import type { MediaImage } from './MediaImage';
import type { Release } from './Release';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type ScheduleMedia = {
    readonly url?: string;
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    name: string;
    readonly artistDisplay?: string;
    readonly artists?: Array<MediaArtist>;
    readonly releases?: Array<Release>;
    readonly image?: MediaImage;
};

