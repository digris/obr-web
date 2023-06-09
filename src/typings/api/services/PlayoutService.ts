/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedPlayoutScheduleList } from '../models/PaginatedPlayoutScheduleList';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PlayoutService {

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedPlayoutScheduleList
     * @throws ApiError
     */
    public static playoutScheduleList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedPlayoutScheduleList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/playout/schedule/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

}
