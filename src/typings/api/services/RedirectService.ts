/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RedirectService {

    /**
     * @param objCt
     * @param objUid
     * @returns void
     * @throws ApiError
     */
    public static redirectObpRetrieve(
        objCt: string,
        objUid: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/redirect/obp/{objCt}:{objUid}/',
            path: {
                'objCt': objCt,
                'objUid': objUid,
            },
            errors: {
                301: `No response body`,
                302: `No response body`,
            },
        });
    }

}