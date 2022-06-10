/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Image } from './Image';

export type Release = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    name: string;
    readonly numMedia?: number;
    readonly image?: Image;
};

