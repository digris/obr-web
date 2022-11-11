/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Settings } from '../models/Settings';
import type { Version } from '../models/Version';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class BaseService {

    /**
     * @returns Settings
     * @throws ApiError
     */
    public static settings(): CancelablePromise<Settings> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/base/settings/',
        });
    }

    /**
     * @returns Version
     * @throws ApiError
     */
    public static version(): CancelablePromise<Version> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/base/version/',
        });
    }

}
