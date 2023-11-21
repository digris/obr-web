/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { VoteScopeEnum } from './VoteScopeEnum';
import type { VoteSourceEnum } from './VoteSourceEnum';

export type VoteWriteRequest = {
  key: string;
  value: number | null;
  source?: VoteSourceEnum | null;
  scope?: VoteScopeEnum | null;
  comment?: string;
};

