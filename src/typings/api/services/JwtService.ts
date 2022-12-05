/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TokenObtainSliding } from '../models/TokenObtainSliding';
import type { TokenObtainSlidingRequest } from '../models/TokenObtainSlidingRequest';
import type { TokenRefreshSliding } from '../models/TokenRefreshSliding';
import type { TokenRefreshSlidingRequest } from '../models/TokenRefreshSlidingRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class JwtService {

    /**
     * Takes a set of user credentials and returns a sliding JSON web token to
     * prove the authentication of those credentials.
     * @param requestBody
     * @returns TokenObtainSliding
     * @throws ApiError
     */
    public static jwtCreate(
        requestBody: TokenObtainSlidingRequest,
    ): CancelablePromise<TokenObtainSliding> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/jwt/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Takes a sliding JSON web token and returns a new, refreshed version if the
     * token's refresh period has not expired.
     * @param requestBody
     * @returns TokenRefreshSliding
     * @throws ApiError
     */
    public static jwtRefreshCreate(
        requestBody: TokenRefreshSlidingRequest,
    ): CancelablePromise<TokenRefreshSliding> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/jwt/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
