/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Playlist } from './Playlist';

export type PaginatedPlaylistList = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: Array<Playlist>;
};

