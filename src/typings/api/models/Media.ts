/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MediaArtist } from './MediaArtist';
import type { Release } from './Release';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Media = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    name: string;
    readonly artistDisplay?: string;
    readonly artists?: Array<MediaArtist>;
    readonly releases?: Array<Release>;
    readonly latestAirplay?: string | null;
    readonly numAirplays?: number | null;
    readonly userRating?: number | null;
    readonly fadeIn?: number;
    readonly fadeOut?: number;
    readonly cueIn?: number;
    readonly cueOut?: number;
};

