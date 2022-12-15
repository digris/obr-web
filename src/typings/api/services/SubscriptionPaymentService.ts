/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Payment } from '../models/Payment';
import type { PaymentCreateRequest } from '../models/PaymentCreateRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SubscriptionPaymentService {

    /**
     * @returns void
     * @throws ApiError
     */
    public static stripeGetPayment(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/stripe/',
        });
    }

    /**
     * @param requestBody
     * @returns Payment
     * @throws ApiError
     */
    public static stripeCreatePayment(
        requestBody: PaymentCreateRequest,
    ): CancelablePromise<Payment> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/payment/stripe/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @param signedPaymentUid
     * @returns void
     * @throws ApiError
     */
    public static stripePaymentSuccess(
        signedPaymentUid: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/stripe/success/{signedPaymentUid}/',
            path: {
                'signedPaymentUid': signedPaymentUid,
            },
            errors: {
                301: `No response body`,
                302: `No response body`,
            },
        });
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static stripePaymentWebhook(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/payment/stripe/webhook/',
        });
    }

}
