/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { VoteWrite } from '../models/VoteWrite';
import type { VoteWriteRequest } from '../models/VoteWriteRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RatingService {

    /**
     * @param objCt
     * @param objUid
     * @returns VoteWrite
     * @throws ApiError
     */
    public static ratingRetrieve(
        objCt: string,
        objUid: string,
    ): CancelablePromise<VoteWrite> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/rating/{objCt}:{objUid}/',
            path: {
                'objCt': objCt,
                'objUid': objUid,
            },
        });
    }

    /**
     * @param objCt
     * @param objUid
     * @param requestBody
     * @returns VoteWrite
     * @throws ApiError
     */
    public static ratingCreate(
        objCt: string,
        objUid: string,
        requestBody: VoteWriteRequest,
    ): CancelablePromise<VoteWrite> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/rating/{objCt}:{objUid}/',
            path: {
                'objCt': objCt,
                'objUid': objUid,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @param objCt
     * @param objUid
     * @returns void
     * @throws ApiError
     */
    public static ratingDestroy(
        objCt: string,
        objUid: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/rating/{objCt}:{objUid}/',
            path: {
                'objCt': objCt,
                'objUid': objUid,
            },
        });
    }

}
