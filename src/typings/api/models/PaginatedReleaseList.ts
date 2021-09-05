/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Release } from './Release';

export type PaginatedReleaseList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Release>;
}
