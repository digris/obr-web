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
     * @param formData
     * @returns TokenObtainSliding
     * @throws ApiError
     */
    public static jwtCreate(
        formData: TokenObtainSlidingRequest,
    ): CancelablePromise<TokenObtainSliding> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/jwt/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * Takes a sliding JSON web token and returns a new, refreshed version if the
     * token's refresh period has not expired.
     * @param formData
     * @returns TokenRefreshSliding
     * @throws ApiError
     */
    public static jwtRefreshCreate(
        formData: TokenRefreshSlidingRequest,
    ): CancelablePromise<TokenRefreshSliding> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/jwt/refresh/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

}
