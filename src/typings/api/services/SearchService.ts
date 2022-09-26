/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedSearchMediaResultList } from '../models/PaginatedSearchMediaResultList';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SearchService {

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedSearchMediaResultList
     * @throws ApiError
     */
    public static searchGlobalMediaList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedSearchMediaResultList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/global/media/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

}
