/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class PubSubBridgeService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async pubSubBridgeCreate(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/pub-sub-bridge/`,
        });
        return result.body;
    }

}