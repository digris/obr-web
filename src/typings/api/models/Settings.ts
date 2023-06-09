/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MediaEndpoints } from './MediaEndpoints';
import type { StreamEndpoints } from './StreamEndpoints';

export type Settings = {
    readonly IMAGE_RESIZER_ENDPOINT: string;
    readonly STREAM_ENDPOINTS: StreamEndpoints;
    readonly STREAM_LATENCY: number;
    readonly MEDIA_ENDPOINTS: MediaEndpoints;
    readonly SENTRY_DSN: string;
};

