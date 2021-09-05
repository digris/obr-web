/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class SubscriptionService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionPaymentRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/subscription/payment/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionPaymentStripeRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/subscription/payment/stripe/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionPaymentStripeCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/subscription/payment/stripe/`,
        });
        return result.body;
    }

    /**
     * @param signedPaymentUid
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionPaymentStripeSuccessRetrieve(
        signedPaymentUid: string,
    ): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/subscription/payment/stripe/success/${signedPaymentUid}/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionPaymentStripeWebhookCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/subscription/payment/stripe/webhook/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionPlanRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/subscription/plan/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionVoucherRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/subscription/voucher/`,
        });
        return result.body;
    }

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async subscriptionVoucherCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/subscription/voucher/`,
        });
        return result.body;
    }

}