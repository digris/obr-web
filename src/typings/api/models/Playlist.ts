/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlaylistEditor } from './PlaylistEditor';
import type { PlaylistEmission } from './PlaylistEmission';
import type { PlaylistImage } from './PlaylistImage';
import type { PlaylistMedia } from './PlaylistMedia';
import type { PlaylistSeries } from './PlaylistSeries';
import type { Tag } from './Tag';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Playlist = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  readonly url: string;
  name?: string;
  readonly series: PlaylistSeries;
  readonly latestEmissionTimeStart: string;
  readonly userRatingTimeRated: string;
  readonly numMedia: number;
  readonly image: PlaylistImage | null;
  readonly userRating: number | null;
  readonly emissions: Array<PlaylistEmission>;
  readonly mediaSet: Array<PlaylistMedia>;
  readonly latestEmission: PlaylistEmission;
  readonly tags: Array<Tag>;
  readonly duration: number;
  readonly editor: PlaylistEditor;
};

