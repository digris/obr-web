/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class RatingService {

    /**
     * @param objCt
     * @param objUid
     * @returns any No response body
     * @throws ApiError
     */
    public static async ratingRetrieve(
        objCt: string,
        objUid: string,
    ): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/rating/${objCt}:${objUid}/`,
        });
        return result.body;
    }

    /**
     * @param objCt
     * @param objUid
     * @returns any No response body
     * @throws ApiError
     */
    public static async ratingCreate(
        objCt: string,
        objUid: string,
    ): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/rating/${objCt}:${objUid}/`,
        });
        return result.body;
    }

}