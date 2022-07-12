/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EmissionMedia } from './EmissionMedia';

export type EmissionMediaSet = {
    uid: string;
    cueIn: number;
    cueOut: number;
    fadeIn: number;
    fadeOut: number;
    fadeCross: number;
    timeStart: string;
    timeEnd: string;
    media: EmissionMedia;
};

