/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Mood } from './Mood';

export type PaginatedMoodList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Mood>;
}
