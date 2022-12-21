/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Artist } from '../models/Artist';
import type { CatalogPlaylist } from '../models/CatalogPlaylist';
import type { Media } from '../models/Media';
import type { Mood } from '../models/Mood';
import type { PaginatedArtistList } from '../models/PaginatedArtistList';
import type { PaginatedCatalogPlaylistList } from '../models/PaginatedCatalogPlaylistList';
import type { PaginatedMediaList } from '../models/PaginatedMediaList';
import type { PaginatedMoodList } from '../models/PaginatedMoodList';
import type { PaginatedReleaseList } from '../models/PaginatedReleaseList';
import type { Release } from '../models/Release';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CatalogService {

    /**
     * Artist endpoint.
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @param userRating
     * @returns PaginatedArtistList
     * @throws ApiError
     */
    public static catalogArtistsList(
        limit?: number,
        offset?: number,
        userRating?: number,
    ): CancelablePromise<PaginatedArtistList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/artists/',
            query: {
                'limit': limit,
                'offset': offset,
                'user_rating': userRating,
            },
        });
    }

    /**
     * Artist endpoint.
     * @param uid
     * @param expand
     * @returns Artist
     * @throws ApiError
     */
    public static catalogArtistsRetrieve(
        uid: string,
        expand?: string,
    ): CancelablePromise<Artist> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/artists/{uid}/',
            path: {
                'uid': uid,
            },
            query: {
                'expand': expand,
            },
        });
    }

    /**
     * Artist endpoint.
     * @returns Artist
     * @throws ApiError
     */
    public static catalogArtistsTagsRetrieve(): CancelablePromise<Artist> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/artists/tags/',
        });
    }

    /**
     * Media endpoint.
     * @param expand Expand nested resources, multiple values possible.
     * @param limit Number of results to return per page.
     * @param objKey Filter media belonging to a related object.
     * format: `<ct>:<uid>`
     * @param offset The initial index from which to return the results.
     * @param userRating Limit results based on current user's rating ❤
     * @returns PaginatedMediaList
     * @throws ApiError
     */
    public static catalogMediaList(
        expand?: Array<'identifiers' | 'image' | 'tags'>,
        limit?: number,
        objKey?: string,
        offset?: number,
        userRating?: -1 | 1,
    ): CancelablePromise<PaginatedMediaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/media/',
            query: {
                'expand': expand,
                'limit': limit,
                'obj_key': objKey,
                'offset': offset,
                'user_rating': userRating,
            },
        });
    }

    /**
     * Media endpoint.
     * @param uid
     * @returns Media
     * @throws ApiError
     */
    public static catalogMediaRetrieve(
        uid: string,
    ): CancelablePromise<Media> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/media/{uid}/',
            path: {
                'uid': uid,
            },
        });
    }

    /**
     * Media endpoint.
     * @returns Media
     * @throws ApiError
     */
    public static catalogMediaTagsRetrieve(): CancelablePromise<Media> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/media/tags/',
        });
    }

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedMoodList
     * @throws ApiError
     */
    public static catalogMoodsList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedMoodList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/moods/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

    /**
     * @param uid
     * @returns Mood
     * @throws ApiError
     */
    public static catalogMoodsRetrieve(
        uid: string,
    ): CancelablePromise<Mood> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/moods/{uid}/',
            path: {
                'uid': uid,
            },
        });
    }

    /**
     * @param limit Number of results to return per page.
     * @param objKey
     * @param offset The initial index from which to return the results.
     * @param userRating
     * @returns PaginatedCatalogPlaylistList
     * @throws ApiError
     */
    public static catalogPlaylistsList(
        limit?: number,
        objKey?: string,
        offset?: number,
        userRating?: number,
    ): CancelablePromise<PaginatedCatalogPlaylistList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/playlists/',
            query: {
                'limit': limit,
                'obj_key': objKey,
                'offset': offset,
                'user_rating': userRating,
            },
        });
    }

    /**
     * @param uid
     * @returns CatalogPlaylist
     * @throws ApiError
     */
    public static catalogPlaylistsRetrieve(
        uid: string,
    ): CancelablePromise<CatalogPlaylist> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/playlists/{uid}/',
            path: {
                'uid': uid,
            },
        });
    }

    /**
     * @returns CatalogPlaylist
     * @throws ApiError
     */
    public static catalogPlaylistsTagsRetrieve(): CancelablePromise<CatalogPlaylist> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/playlists/tags/',
        });
    }

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedReleaseList
     * @throws ApiError
     */
    public static catalogReleasesList(
        limit?: number,
        offset?: number,
    ): CancelablePromise<PaginatedReleaseList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/releases/',
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
    }

    /**
     * @param uid
     * @returns Release
     * @throws ApiError
     */
    public static catalogReleasesRetrieve(
        uid: string,
    ): CancelablePromise<Release> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/catalog/releases/{uid}/',
            path: {
                'uid': uid,
            },
        });
    }

}
