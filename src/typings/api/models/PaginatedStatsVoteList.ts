/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { StatsVote } from './StatsVote';

export type PaginatedStatsVoteList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<StatsVote>;
};

