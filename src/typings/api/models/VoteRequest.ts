/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ScopeEnum } from './ScopeEnum';

export type VoteRequest = {
    key: string;
    value: number | null;
    scope?: ScopeEnum | null;
    comment?: string;
};

