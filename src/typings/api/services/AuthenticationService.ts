/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { LoginRequest } from '../models/LoginRequest';
import type { SendEmailLogin } from '../models/SendEmailLogin';
import type { SendEmailLoginLookup } from '../models/SendEmailLoginLookup';
import type { SendEmailLoginRequest } from '../models/SendEmailLoginRequest';
import type { TokenLoginRequest } from '../models/TokenLoginRequest';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AuthenticationService {

    /**
     * Login user by email & password
     * @param formData
     * @returns User
     * @throws ApiError
     */
    public static login(
        formData: LoginRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/login/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * Destroy user's session
     * @returns any No response body
     * @throws ApiError
     */
    public static logout(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/logout/',
        });
    }

    /**
     * Lookup if provided email can login by token
     * @param email
     * @returns SendEmailLoginLookup
     * @throws ApiError
     */
    public static sendEmailLoginLookup(
        email: string,
    ): CancelablePromise<SendEmailLoginLookup> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/send-email-login/',
            query: {
                'email': email,
            },
        });
    }

    /**
     * Send email with login token to given address
     * @param formData
     * @returns SendEmailLogin
     * @throws ApiError
     */
    public static sendEmailLogin(
        formData: SendEmailLoginRequest,
    ): CancelablePromise<SendEmailLogin> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/send-email-login/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * Login user by signed email.
     * Responds `200` for existing and `201` for created user.
     * @param signedEmail
     * @returns User
     * @throws ApiError
     */
    public static signedEmailLogin(
        signedEmail: string,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/signed-email-login/',
            query: {
                'signed_email': signedEmail,
            },
        });
    }

    /**
     * Login user by email & login token.
     * Responds `200` for existing and `201` for created user.
     * @param formData
     * @returns User
     * @throws ApiError
     */
    public static tokenLogin(
        formData: TokenLoginRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/token-login/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * User endpoint. Empty (204) response for anonymous users.
     * @param expand Expand nested resources, multiple values separated by comma.
     * Available options: `settings`, `address`, `subscription`
     * @returns User
     * @throws ApiError
     */
    public static user(
        expand?: Array<'address' | 'settings' | 'subscription'>,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/users/me/',
            query: {
                'expand': expand,
            },
        });
    }

}
