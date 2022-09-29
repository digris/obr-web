/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ray } from './Ray';
import type { Tag } from './Tag';

export type Mood = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly url?: string;
    readonly name?: string;
    teaser?: string | null;
    readonly tags?: Array<Tag>;
    readonly rgb?: Array<number>;
    readonly rays?: Array<Ray>;
    readonly userRating?: number | null;
};

