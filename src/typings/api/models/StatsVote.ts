/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { VoteScopeEnum } from './VoteScopeEnum';
import type { VoteSourceEnum } from './VoteSourceEnum';

export type StatsVote = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  key: string;
  readonly value: number;
  readonly source: VoteSourceEnum;
  readonly scope: VoteScopeEnum;
  readonly comment: string;
  readonly updated: string;
  readonly isAnonymous: boolean;
  user: string | null;
};

