/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class AccountService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountLoginCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/account/login/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountLogoutCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/account/logout/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountSendEmailLoginRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/account/send-email-login/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountSendEmailLoginCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/account/send-email-login/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountSignedEmailLoginCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/account/signed-email-login/`,
        });
        return result.body;
    }

    /**
     * returns all connected and disconnected social backends.
     * (based on requests current user)
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountSocialBackendsRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/account/social-backends/`,
        });
        return result.body;
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
    public static async accountSocialBackendsDestroy(
        provider: string,
        uid: string,
    ): Promise<void> {
        const result = await __request({
            method: 'DELETE',
            path: `/api/v1/account/social-backends/${provider}/${uid}/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountTokenLoginCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/account/token-login/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async accountUsersMeRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/account/users/me/`,
        });
        return result.body;
    }

}