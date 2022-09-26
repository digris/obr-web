/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Payment } from '../models/Payment';
import type { PaymentCreateRequest } from '../models/PaymentCreateRequest';
import type { PaymentOption } from '../models/PaymentOption';
import type { SubscriptionOption } from '../models/SubscriptionOption';
import type { Voucher } from '../models/Voucher';
import type { VoucherRequest } from '../models/VoucherRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SubscriptionService {

    /**
     * @returns PaymentOption
     * @throws ApiError
     */
    public static subscriptionPaymentRetrieve(): CancelablePromise<PaymentOption> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/',
        });
    }

    /**
     * @returns void
     * @throws ApiError
     */
    public static subscriptionPaymentStripeRetrieve(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/stripe/',
        });
    }

    /**
     * @param formData
     * @returns Payment
     * @throws ApiError
     */
    public static subscriptionPaymentStripeCreate(
        formData: PaymentCreateRequest,
    ): CancelablePromise<Payment> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/payment/stripe/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * @param signedPaymentUid
     * @returns void
     * @throws ApiError
     */
    public static subscriptionPaymentStripeSuccessRetrieve(
        signedPaymentUid: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/stripe/success/{signed_payment_uid}/',
            path: {
                'signed_payment_uid': signedPaymentUid,
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
    public static subscriptionPaymentStripeWebhookCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/payment/stripe/webhook/',
        });
    }

    /**
     * @returns SubscriptionOption
     * @throws ApiError
     */
    public static subscriptionPlanRetrieve(): CancelablePromise<SubscriptionOption> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/plan/',
        });
    }

    /**
     * @returns Voucher
     * @throws ApiError
     */
    public static subscriptionVoucherRetrieve(): CancelablePromise<Voucher> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/voucher/',
        });
    }

    /**
     * @param formData
     * @returns Voucher
     * @throws ApiError
     */
    public static subscriptionVoucherCreate(
        formData?: VoucherRequest,
    ): CancelablePromise<Voucher> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/voucher/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

}
