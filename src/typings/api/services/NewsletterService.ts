/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Newsletter } from '../models/Newsletter';
import type { SubscriptionRequest } from '../models/SubscriptionRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class NewsletterService {

    /**
     * @returns Newsletter
     * @throws ApiError
     */
    public static newsletters(): CancelablePromise<Array<Newsletter>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/newsletter/newsletters/',
        });
    }

    /**
     * @param requestBody
     * @returns Newsletter
     * @throws ApiError
     */
    public static subscribe(
        requestBody: SubscriptionRequest,
    ): CancelablePromise<Array<Newsletter>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/newsletter/newsletters/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
