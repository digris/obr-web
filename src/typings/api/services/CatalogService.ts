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
import { request as __request } from '../core/request';

export class CatalogService {

    /**
     * Artist endpoint.
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedArtistList
     * @throws ApiError
     */
    public static async catalogArtistsList(
        limit?: number,
        offset?: number,
    ): Promise<PaginatedArtistList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/artists/`,
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
        return result.body;
    }

    /**
     * Artist endpoint.
     * @param uid
     * @returns Artist
     * @throws ApiError
     */
    public static async catalogArtistsRetrieve(
        uid: string,
    ): Promise<Artist> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/artists/${uid}/`,
        });
        return result.body;
    }

    /**
     * Media endpoint.
     *
     * retrieve:
     * Returns a media instance.
     *
     * list:
     * Returns all a list of media...
     * @param limit Number of results to return per page.
     * @param objKey
     * @param offset The initial index from which to return the results.
     * @param userRating
     * @returns PaginatedMediaList
     * @throws ApiError
     */
    public static async catalogMediaList(
        limit?: number,
        objKey?: string,
        offset?: number,
        userRating?: number,
    ): Promise<PaginatedMediaList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/media/`,
            query: {
                'limit': limit,
                'obj_key': objKey,
                'offset': offset,
                'user_rating': userRating,
            },
        });
        return result.body;
    }

    /**
     * Media endpoint.
     *
     * retrieve:
     * Returns a media instance.
     *
     * list:
     * Returns all a list of media...
     * @param uid
     * @returns Media
     * @throws ApiError
     */
    public static async catalogMediaRetrieve(
        uid: string,
    ): Promise<Media> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/media/${uid}/`,
        });
        return result.body;
    }

    /**
     * Media endpoint.
     *
     * retrieve:
     * Returns a media instance.
     *
     * list:
     * Returns all a list of media...
     * @returns Media
     * @throws ApiError
     */
    public static async catalogMediaTagsRetrieve(): Promise<Media> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/media/tags/`,
        });
        return result.body;
    }

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedMoodList
     * @throws ApiError
     */
    public static async catalogMoodsList(
        limit?: number,
        offset?: number,
    ): Promise<PaginatedMoodList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/moods/`,
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
        return result.body;
    }

    /**
     * @param uid
     * @returns Mood
     * @throws ApiError
     */
    public static async catalogMoodsRetrieve(
        uid: string,
    ): Promise<Mood> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/moods/${uid}/`,
        });
        return result.body;
    }

    /**
     * @param limit Number of results to return per page.
     * @param objKey
     * @param offset The initial index from which to return the results.
     * @param userRating
     * @returns PaginatedCatalogPlaylistList
     * @throws ApiError
     */
    public static async catalogPlaylistsList(
        limit?: number,
        objKey?: string,
        offset?: number,
        userRating?: number,
    ): Promise<PaginatedCatalogPlaylistList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/playlists/`,
            query: {
                'limit': limit,
                'obj_key': objKey,
                'offset': offset,
                'user_rating': userRating,
            },
        });
        return result.body;
    }

    /**
     * @param uid
     * @returns CatalogPlaylist
     * @throws ApiError
     */
    public static async catalogPlaylistsRetrieve(
        uid: string,
    ): Promise<CatalogPlaylist> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/playlists/${uid}/`,
        });
        return result.body;
    }

    /**
     * @param limit Number of results to return per page.
     * @param offset The initial index from which to return the results.
     * @returns PaginatedReleaseList
     * @throws ApiError
     */
    public static async catalogReleasesList(
        limit?: number,
        offset?: number,
    ): Promise<PaginatedReleaseList> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/releases/`,
            query: {
                'limit': limit,
                'offset': offset,
            },
        });
        return result.body;
    }

    /**
     * @param uid
     * @returns Release
     * @throws ApiError
     */
    public static async catalogReleasesRetrieve(
        uid: string,
    ): Promise<Release> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/catalog/releases/${uid}/`,
        });
        return result.body;
    }

}