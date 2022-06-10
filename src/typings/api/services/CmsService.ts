/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CmsService {

    /**
     * @param path
     * @returns any No response body
     * @throws ApiError
     */
    public static cmsPageRetrieve(
        path: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/cms/page/{path}/',
            path: {
                'path': path,
            },
        });
    }

}
