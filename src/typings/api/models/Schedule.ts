/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ScheduleEmission } from './ScheduleEmission';
import type { ScheduleMedia } from './ScheduleMedia';
import type { SchedulePlaylist } from './SchedulePlaylist';

export type Schedule = {
    readonly key?: string;
    readonly cueIn?: number;
    readonly cueOut?: number;
    readonly fadeIn?: number;
    readonly fadeOut?: number;
    readonly fadeCross?: number;
    readonly timeStart?: string;
    readonly timeEnd?: string;
    readonly media?: ScheduleMedia;
    readonly emission?: ScheduleEmission;
    readonly playlist?: SchedulePlaylist;
};

