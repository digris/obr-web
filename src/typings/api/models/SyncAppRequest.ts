/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AppLabelsEnum } from './AppLabelsEnum';

export type SyncAppRequest = {
    appLabels: Array<AppLabelsEnum>;
    /**
     * limit number if items per app to sync each run
     */
    limit?: number | null;
    /**
     * max age / last time updated before n seconds
     */
    maxAge?: number | null;
};

