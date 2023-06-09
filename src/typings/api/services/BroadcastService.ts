/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Editor } from '../models/Editor';
import type { Emission } from '../models/Emission';
import type { PaginatedEditorList } from '../models/PaginatedEditorList';
import type { PaginatedEmissionList } from '../models/PaginatedEmissionList';
import type { PaginatedScheduleList } from '../models/PaginatedScheduleList';
import type { Program } from '../models/Program';

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
     * @param expand
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @param timeFrom
     * @param timeUntil See `time_from` for examples.
     * @returns PaginatedEmissionList
     * @throws ApiError
     */
    public static broadcastEmissionsList(
        expand?: Array<'live_ratings' | 'media_set'>,
        limit?: number,
        offset?: number,
        timeFrom?: string,
        timeUntil?: string,
    ): CancelablePromise<PaginatedEmissionList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/emissions/',
            query: {
                'expand': expand,
                'limit': limit,
                'offset': offset,
                'time_from': timeFrom,
                'time_until': timeUntil,
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
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedScheduleList
     * @throws ApiError
     */
    public static broadcastScheduleList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedScheduleList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/broadcast/schedule/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

}
