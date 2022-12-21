/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { VoteScopeEnum } from './VoteScopeEnum';

export type VoteRequest = {
    key: string;
    value: number | null;
    scope?: VoteScopeEnum | null;
    comment?: string;
};

