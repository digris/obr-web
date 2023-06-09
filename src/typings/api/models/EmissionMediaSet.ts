/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EmissionMedia } from './EmissionMedia';

export type EmissionMediaSet = {
    readonly uid: string;
    readonly cueIn: number;
    readonly cueOut: number;
    readonly fadeIn: number;
    readonly fadeOut: number;
    readonly fadeCross: number;
    readonly timeStart: string;
    readonly timeEnd: string;
    readonly media: EmissionMedia;
};

