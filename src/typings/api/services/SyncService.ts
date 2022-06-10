/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SyncSchedule } from '../models/SyncSchedule';
import type { SyncScheduleRequest } from '../models/SyncScheduleRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SyncService {

    /**
     * @param formData
     * @returns SyncSchedule
     * @throws ApiError
     */
    public static syncScheduleCreate(
        formData?: SyncScheduleRequest,
    ): CancelablePromise<SyncSchedule> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/sync/schedule/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

}
