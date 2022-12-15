/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaymentOption } from '../models/PaymentOption';
import type { SubscriptionOption } from '../models/SubscriptionOption';
import type { UserVoucher } from '../models/UserVoucher';
import type { Voucher } from '../models/Voucher';
import type { VoucherRequest } from '../models/VoucherRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SubscriptionService {

    /**
     * Get available payment options.
     * @returns PaymentOption
     * @throws ApiError
     */
    public static paymentOptions(): CancelablePromise<PaymentOption> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/payment/',
        });
    }

    /**
     * Get available plan options.
     * @returns SubscriptionOption
     * @throws ApiError
     */
    public static planOptions(): CancelablePromise<SubscriptionOption> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/plan/',
        });
    }

    /**
     * Vouchers that user can provide to other people.
     * @returns UserVoucher
     * @throws ApiError
     */
    public static userVouchers(): CancelablePromise<Array<UserVoucher>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/user-vouchers/',
        });
    }

    /**
     * Check validity of a voucher for the current user.
     * @returns Voucher
     * @throws ApiError
     */
    public static checkVoucher(): CancelablePromise<Voucher> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/subscription/voucher/',
        });
    }

    /**
     * Redeem a voucher for the current user.
     * @param requestBody
     * @returns Voucher
     * @throws ApiError
     */
    public static redeemVoucher(
        requestBody?: VoucherRequest,
    ): CancelablePromise<Voucher> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/subscription/voucher/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
