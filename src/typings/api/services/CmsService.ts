/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page } from '../models/Page';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CmsService {

    /**
     * @param path
     * @returns Page
     * @throws ApiError
     */
    public static page(
        path: string,
    ): CancelablePromise<Page> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/cms/page/{path}/',
            path: {
                'path': path,
            },
        });
    }

}
