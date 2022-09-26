/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ray } from './Ray';
import type { Tag } from './Tag';

export type Mood = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    name: string;
    teaser?: string | null;
    tags: Array<Tag>;
    readonly rgb?: Array<number>;
    readonly rays?: Array<Ray>;
    readonly userRating?: number | null;
};

