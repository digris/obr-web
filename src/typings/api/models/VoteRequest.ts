/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { VoteScopeEnum } from './VoteScopeEnum';
import type { VoteSourceEnum } from './VoteSourceEnum';

export type VoteRequest = {
    key: string;
    value: number | null;
    source?: VoteSourceEnum | null;
    scope?: VoteScopeEnum | null;
    comment?: string;
};

