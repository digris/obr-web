/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Archive } from '../models/Archive';
import type { PlayerEventCreateRequest } from '../models/PlayerEventCreateRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StatsService {

    /**
     * Archives `Emissions` & `Air-plays`.
     * This resource is periodically requested by GCP Cloud Scheduler.
     * Invoking requires `account.api_stats_webhooks` permissions.
     * @returns Archive
     * @throws ApiError
     */
    public static statsArchive(): CancelablePromise<Archive> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/stats/archive/',
        });
    }

    /**
     * Ingest Player-event
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static statsPlayerEvent(
        requestBody: Array<PlayerEventCreateRequest>,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/stats/player-events/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
