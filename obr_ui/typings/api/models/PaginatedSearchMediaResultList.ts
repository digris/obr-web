/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SearchMediaResult } from './SearchMediaResult';

export type PaginatedSearchMediaResultList = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: Array<SearchMediaResult>;
};

