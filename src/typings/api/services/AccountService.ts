/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AccountService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountAddressPartialUpdate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/account/address/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountEmailCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/email/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountLoginCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/login/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountLogoutCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/logout/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountPasswordCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/password/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountSendEmailLoginRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/send-email-login/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountSendEmailLoginCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/send-email-login/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountSignedEmailLoginCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/signed-email-login/',
        });
    }

    /**
     * returns all connected and disconnected social backends.
     * (based on requests current user)
     * @returns any No response body
     * @throws ApiError
     */
    public static accountSocialBackendsRetrieve(): CancelablePromise<any> {
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
    public static accountSocialBackendsDestroy(
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
     * @returns any No response body
     * @throws ApiError
     */
    public static accountTokenLoginCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/account/token-login/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountUsersMeRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/account/users/me/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static accountUsersMePartialUpdate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/account/users/me/',
        });
    }

}
