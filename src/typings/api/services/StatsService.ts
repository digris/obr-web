/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlayerEvent } from '../models/PlayerEvent';
import type { PlayerEventRequest } from '../models/PlayerEventRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StatsService {

    /**
     * @param formData
     * @returns PlayerEvent
     * @throws ApiError
     */
    public static statsPlayerEventsUpdate(
        formData: PlayerEventRequest,
    ): CancelablePromise<PlayerEvent> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/stats/player-events/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

}
