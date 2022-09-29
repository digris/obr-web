/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Editor } from '../models/Editor';
import type { Emission } from '../models/Emission';
import type { PaginatedEditorList } from '../models/PaginatedEditorList';
import type { Program } from '../models/Program';
import type { Schedule } from '../models/Schedule';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class BroadcastService {

    /**
     * @param expand
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedEditorList
     * @throws ApiError
     */
    public static broadcastEditorsList(
        expand?: Array<'identifiers' | 'tags'>,
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedEditorList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/editors/',
            query: {
                'expand': expand,
                'limit': limit,
                'offset': offset,
            },
        });
    }

    /**
     * @param uid
     * @param expand
     * @returns Editor
     * @throws ApiError
     */
    public static broadcastEditorsRetrieve(
        uid: string,
        expand?: Array<'identifiers' | 'tags'>,
    ): CancelablePromise<Editor> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/editors/{uid}/',
            path: {
                'uid': uid,
            },
            query: {
                'expand': expand,
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
     * @param date Defaults to the current date.
     * A day is considered to start at `06:00 CET`
     * @returns Program
     * @throws ApiError
     */
    public static broadcastProgramRetrieve(
        date?: string,
    ): CancelablePromise<Program> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/program/',
            query: {
                'date': date,
            },
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

}
