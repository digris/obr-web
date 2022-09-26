/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EmailUpdateRequest } from '../models/EmailUpdateRequest';
import type { LoginRequest } from '../models/LoginRequest';
import type { PasswordUpdateRequest } from '../models/PasswordUpdateRequest';
import type { PatchedAddressRequest } from '../models/PatchedAddressRequest';
import type { PatchedUserRequest } from '../models/PatchedUserRequest';
import type { SendEmailLogin } from '../models/SendEmailLogin';
import type { SendEmailLoginLookup } from '../models/SendEmailLoginLookup';
import type { SendEmailLoginRequest } from '../models/SendEmailLoginRequest';
import type { SocialBackends } from '../models/SocialBackends';
import type { TokenLoginRequest } from '../models/TokenLoginRequest';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AccountService {

    /**
     * @param formData
     * @returns void
     * @throws ApiError
     */
    public static userUpdateAddress(
        formData?: PatchedAddressRequest,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/account/address/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * Update or set email address
     * @param formData
     * @returns void
     * @throws ApiError
     */
    public static userUpdateEmail(
        formData: EmailUpdateRequest,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/email/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

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
     * Update or set password
     * @param formData
     * @returns void
     * @throws ApiError
     */
    public static userUpdatePassword(
        formData: PasswordUpdateRequest,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/password/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
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
     * Login user by signed email
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
     * returns all connected and disconnected social backends.
     * (based on requests current user)
     * @returns SocialBackends
     * @throws ApiError
     */
    public static socialBackends(): CancelablePromise<SocialBackends> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/social-backends/',
        });
    }

    /**
     * single backend association.
     * (based on requests current user)
     * this resource is only used to "disconnect" from a backend.
     * @param provider
     * @param uid
     * @returns void
     * @throws ApiError
     */
    public static socialBackendDisconnect(
        provider: string,
        uid: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/account/social-backends/{provider}/{uid}/',
            path: {
                'provider': provider,
                'uid': uid,
            },
        });
    }

    /**
     * Login user by email & token [ABC-DEF]
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
     * Get current user
     * @returns User
     * @throws ApiError
     */
    public static user(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/users/me/',
        });
    }

    /**
     * @param formData
     * @returns User
     * @throws ApiError
     */
    public static userPartialUpdate(
        formData?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/account/users/me/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

}
