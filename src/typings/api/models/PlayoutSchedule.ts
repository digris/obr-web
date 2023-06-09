/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlayoutScheduleMedia } from './PlayoutScheduleMedia';
import type { ScheduleMaster } from './ScheduleMaster';

export type PlayoutSchedule = {
  uid: string;
  key: string;
  cueIn: number;
  cueOut: number;
  fadeIn: number;
  fadeOut: number;
  fadeCross: number;
  timeStart: string;
  timeEnd: string;
  duration: number;
  media: PlayoutScheduleMedia;
  master: ScheduleMaster;
};

