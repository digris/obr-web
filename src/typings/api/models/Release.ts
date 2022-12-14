/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ReleaseImage } from './ReleaseImage';

export type Release = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly url?: string;
    readonly name?: string;
    readonly numMedia?: number;
    readonly isNew?: boolean;
    readonly image?: ReleaseImage | null;
};

