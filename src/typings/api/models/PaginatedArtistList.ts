/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Artist } from './Artist';

export type PaginatedArtistList = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: Array<Artist>;
};

