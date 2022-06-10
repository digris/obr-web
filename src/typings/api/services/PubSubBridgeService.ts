/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PubSubBridgeService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static pubSubBridgeCreate(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/pub-sub-bridge/',
        });
    }

}
