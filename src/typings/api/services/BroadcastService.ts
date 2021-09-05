/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Editor } from '../models/Editor';
import type { Emission } from '../models/Emission';
import type { PaginatedEditorList } from '../models/PaginatedEditorList';
import type { PaginatedEmissionList } from '../models/PaginatedEmissionList';
import type { Program } from '../models/Program';
import type { Schedule } from '../models/Schedule';
import { request as __request } from '../core/request';

export class BroadcastService {

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedEditorList
     * @throws ApiError
     */
    public static async broadcastEditorsList(
        limit?: number,
        offset?: number,
    ): Promise<PaginatedEditorList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/broadcast/editors/`,
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
        return result.body;
    }

    /**
     * @param uid
     * @returns Editor
     * @throws ApiError
     */
    public static async broadcastEditorsRetrieve(
        uid: string,
    ): Promise<Editor> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/broadcast/editors/${uid}/`,
        });
        return result.body;
    }

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedEmissionList
     * @throws ApiError
     */
    public static async broadcastEmissionsList(
        limit?: number,
        offset?: number,
    ): Promise<PaginatedEmissionList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/broadcast/emissions/`,
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
        return result.body;
    }

    /**
     * @param uid
     * @returns Emission
     * @throws ApiError
     */
    public static async broadcastEmissionsRetrieve(
        uid: string,
    ): Promise<Emission> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/broadcast/emissions/${uid}/`,
        });
        return result.body;
    }

    /**
     * @returns Program
     * @throws ApiError
     */
    public static async broadcastProgramRetrieve(): Promise<Program> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/broadcast/program/`,
        });
        return result.body;
    }

    /**
     * @returns Schedule
     * @throws ApiError
     */
    public static async broadcastScheduleRetrieve(): Promise<Schedule> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/broadcast/schedule/`,
        });
        return result.body;
    }

}