/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Editor } from '../models/Editor';
import type { Emission } from '../models/Emission';
import type { PaginatedEditorList } from '../models/PaginatedEditorList';
import type { PaginatedEmissionList } from '../models/PaginatedEmissionList';
import type { Program } from '../models/Program';
import type { Schedule } from '../models/Schedule';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class BroadcastService {

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedEditorList
     * @throws ApiError
     */
    public static broadcastEditorsList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedEditorList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/editors/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

    /**
     * @param uid
     * @returns Editor
     * @throws ApiError
     */
    public static broadcastEditorsRetrieve(
        uid: string,
    ): CancelablePromise<Editor> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/editors/{uid}/',
            path: {
                'uid': uid,
            },
        });
    }

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedEmissionList
     * @throws ApiError
     */
    public static broadcastEmissionsList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedEmissionList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/emissions/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

    /**
     * @param uid
     * @returns Emission
     * @throws ApiError
     */
    public static broadcastEmissionsRetrieve(
        uid: string,
    ): CancelablePromise<Emission> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/emissions/{uid}/',
            path: {
                'uid': uid,
            },
        });
    }

    /**
     * @returns Program
     * @throws ApiError
     */
    public static broadcastProgramRetrieve(): CancelablePromise<Program> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/program/',
        });
    }

    /**
     * @returns Schedule
     * @throws ApiError
     */
    public static broadcastScheduleRetrieve(): CancelablePromise<Schedule> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/schedule/',
        });
    }

    /**
     * @returns Program
     * @throws ApiError
     */
    public static broadcastStationTimeRetrieve(): CancelablePromise<Program> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/station-time/',
        });
    }

}
