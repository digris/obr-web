/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Vote } from '../models/Vote';
import type { VoteRequest } from '../models/VoteRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RatingService {

    /**
     * @param objCt
     * @param objUid
     * @returns Vote
     * @throws ApiError
     */
    public static ratingRetrieve(
        objCt: string,
        objUid: string,
    ): CancelablePromise<Vote> {
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
     * @param formData
     * @returns Vote
     * @throws ApiError
     */
    public static ratingCreate(
        objCt: string,
        objUid: string,
        formData: VoteRequest,
    ): CancelablePromise<Vote> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/rating/{objCt}:{objUid}/',
            path: {
                'objCt': objCt,
                'objUid': objUid,
            },
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

}
