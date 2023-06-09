/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlayoutSchedule } from './PlayoutSchedule';

export type PaginatedPlayoutScheduleList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<PlayoutSchedule>;
};

