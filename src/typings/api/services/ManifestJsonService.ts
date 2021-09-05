/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class ManifestJsonService {

    /**
     * @returns any No response body
     * @throws ApiError
     */
    public static async manifestJsonRetrieve(): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/manifest.json`,
        });
        return result.body;
    }

}