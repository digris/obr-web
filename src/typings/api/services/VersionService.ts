/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Version } from '../models/Version';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class VersionService {

    /**
     * @returns Version
     * @throws ApiError
     */
    public static versionRetrieve(): CancelablePromise<Version> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/version/',
        });
    }

}
