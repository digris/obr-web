/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Media } from './Media';

export type PlaylistMedia = {
  readonly media: Media;
  position?: number;
  cueIn?: number;
  cueOut?: number;
  fadeIn?: number;
  fadeOut?: number;
  fadeCross?: number;
};

