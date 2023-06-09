/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ArtistImage } from './ArtistImage';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Artist = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  readonly url: string;
  readonly name: string;
  readonly numMedia: number;
  readonly mediaTotalDuration: number;
  readonly image: ArtistImage | null;
  countryCode?: string;
  dateStart?: string | null;
  dateEnd?: string | null;
  readonly userRating: number | null;
};

