/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Address } from '../models/Address';
import type { AddressCountries } from '../models/AddressCountries';
import type { EmailUpdateRequest } from '../models/EmailUpdateRequest';
import type { PasswordUpdateRequest } from '../models/PasswordUpdateRequest';
import type { PatchedAddressRequest } from '../models/PatchedAddressRequest';
import type { PatchedUserRequest } from '../models/PatchedUserRequest';
import type { SocialBackends } from '../models/SocialBackends';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AccountService {

    /**
     * @param requestBody
     * @returns Address
     * @throws ApiError
     */
    public static userUpdateAddress(
        requestBody?: PatchedAddressRequest,
    ): CancelablePromise<Address> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/account/address/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns AddressCountries
     * @throws ApiError
     */
    public static addressCountries(): CancelablePromise<Array<AddressCountries>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/address-countries/',
        });
    }

    /**
     * Update or set email address
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static userUpdateEmail(
        requestBody: EmailUpdateRequest,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/email/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Update or set password
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static userUpdatePassword(
        requestBody: PasswordUpdateRequest,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/password/',
            body: requestBody,
            mediaType: 'application/json',
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

    /**
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static userPartialUpdate(
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/account/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
