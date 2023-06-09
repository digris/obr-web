/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Archive } from '../models/Archive';
import type { PaginatedStatsVoteList } from '../models/PaginatedStatsVoteList';
import type { PlayerEventCreateRequest } from '../models/PlayerEventCreateRequest';
import type { StreamEventRequest } from '../models/StreamEventRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StatsService {

    /**
     * Archives `Emissions` & `Air-plays`.
     * This resource is periodically requested by GCP Cloud Scheduler.
     * Invoking requires `account.api_stats_webhooks` permissions.
     * @returns Archive
     * @throws ApiError
     */
    public static statsArchive(): CancelablePromise<Archive> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/stats/archive/',
        });
    }

    /**
     * Ingest Player-event
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static statsPlayerEvent(
        requestBody: Array<PlayerEventCreateRequest>,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/stats/player-events/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @param forYear
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @param scope * `` - not specified
     * * `track` - track
     * * `emission` - emission
     * * `daytime` - daytime
     * * `repetition` - repetition
     * * `genre` - genre
     *
     * * `` - not specified
     * * `track` - track
     * * `emission` - emission
     * * `daytime` - daytime
     * * `repetition` - repetition
     * * `genre` - genre
     * @param source * `live` - live
     * * `ondemand` - on demand
     *
     * * `live` - live
     * * `ondemand` - on demand
     * @param timeFrom
     * @param value * `-1` - -
     * * `1` - +
     *
     * * `-1` - -
     * * `1` - +
     * @returns PaginatedStatsVoteList
     * @throws ApiError
     */
    public static statsRatingsList(
        forYear?: number,
        limit?: number,
        offset?: number,
        scope?: '' | 'daytime' | 'emission' | 'genre' | 'repetition' | 'track',
        source?: 'live' | 'ondemand',
        timeFrom?: string,
        value?: -1 | 1,
    ): CancelablePromise<PaginatedStatsVoteList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/stats/ratings/',
            query: {
                'for_year': forYear,
                'limit': limit,
                'offset': offset,
                'scope': scope,
                'source': source,
                'time_from': timeFrom,
                'value': value,
            },
        });
    }

    /**
     * Ingest 'stream-events' from icecast server
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static statsStreamEvent(
        requestBody: StreamEventRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/stats/stream-events/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
