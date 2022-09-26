/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { NullEnum } from './NullEnum';
import type { ScopeEnum } from './ScopeEnum';

export type VoteRequest = {
    key: string;
    value: number | null;
    scope?: (ScopeEnum | NullEnum) | null;
    comment?: string;
};

