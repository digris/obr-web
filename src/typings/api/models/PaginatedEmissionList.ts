/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Emission } from './Emission';

export type PaginatedEmissionList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Emission>;
}
