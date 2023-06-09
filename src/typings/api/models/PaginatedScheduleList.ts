/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Schedule } from './Schedule';

export type PaginatedScheduleList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Schedule>;
};

