/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SubscriptionService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionPaymentRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionPaymentStripeRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/stripe/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionPaymentStripeCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/payment/stripe/',
        });
    }

    /**
     * @param signedPaymentUid
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionPaymentStripeSuccessRetrieve(
        signedPaymentUid: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/stripe/success/{signed_payment_uid}/',
            path: {
                'signed_payment_uid': signedPaymentUid,
            },
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionPaymentStripeWebhookCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/payment/stripe/webhook/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionPlanRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/plan/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionVoucherRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/voucher/',
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static subscriptionVoucherCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/voucher/',
        });
    }

}
