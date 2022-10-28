/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedCategoryList } from '../models/PaginatedCategoryList';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class FaqService {

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedCategoryList
     * @throws ApiError
     */
    public static faqCategoriesList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedCategoryList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/faq/categories/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

}
