/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ScheduleEmission } from './ScheduleEmission';
import type { ScheduleMedia } from './ScheduleMedia';
import type { SchedulePlaylist } from './SchedulePlaylist';

export type Schedule = {
    key: string;
    cueIn: number;
    cueOut: number;
    fadeIn: number;
    fadeOut: number;
    fadeCross: number;
    timeStart: string;
    timeEnd: string;
    media: ScheduleMedia;
    emission: ScheduleEmission;
    playlist: SchedulePlaylist;
};

