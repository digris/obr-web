/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SyncApp } from '../models/SyncApp';
import type { SyncAppRequest } from '../models/SyncAppRequest';
import type { SyncSchedule } from '../models/SyncSchedule';
import type { SyncScheduleRequest } from '../models/SyncScheduleRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SyncService {

    /**
     * Synchronize sync-enabled models with remote data.
     * This resource is periodically requested by GCP Cloud Scheduler.
     * Invoking requires `account.api_sync_webhooks` permissions.
     * @param requestBody
     * @returns SyncApp
     * @throws ApiError
     */
    public static syncApp(
        requestBody: SyncAppRequest,
    ): CancelablePromise<SyncApp> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/sync/app/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Synchronize schedule with scheduler planning data.
     * This resource is periodically requested by GCP Cloud Scheduler
     * @param requestBody
     * @returns SyncSchedule
     * @throws ApiError
     */
    public static syncSchedule(
        requestBody?: SyncScheduleRequest,
    ): CancelablePromise<SyncSchedule> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/sync/schedule/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
