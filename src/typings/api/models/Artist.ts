/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Image } from './Image';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Artist = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    name: string;
    readonly numMedia?: number;
    readonly image?: Image;
    countryCode?: string | null;
    dateStart?: string | null;
    dateEnd?: string | null;
    readonly userRating?: number | null;
};

