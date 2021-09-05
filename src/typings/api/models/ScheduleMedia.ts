/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MediaArtist } from './MediaArtist';
import type { Release } from './Release';

export type ScheduleMedia = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    name: string;
    readonly artistDisplay?: string;
    readonly artists?: Array<MediaArtist>;
    readonly releases?: Array<Release>;
}
