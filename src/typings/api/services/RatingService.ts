/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RatingService {

    /**
     * @param objCt
     * @param objUid
     * @returns any No response body
     * @throws ApiError
     */
    public static ratingRetrieve(
        objCt: string,
        objUid: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/rating/{obj_ct}:{obj_uid}/',
            path: {
                'obj_ct': objCt,
                'obj_uid': objUid,
            },
        });
    }

    /**
     * @param objCt
     * @param objUid
     * @returns any No response body
     * @throws ApiError
     */
    public static ratingCreate(
        objCt: string,
        objUid: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/rating/{obj_ct}:{obj_uid}/',
            path: {
                'obj_ct': objCt,
                'obj_uid': objUid,
            },
        });
    }

}
