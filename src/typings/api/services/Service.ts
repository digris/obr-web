/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class Service {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async rootRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/`,
        });
        return result.body;
    }

}