/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Media } from './Media';

export type PaginatedMediaList = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: Array<Media>;
};

