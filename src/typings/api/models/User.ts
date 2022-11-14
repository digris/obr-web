/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CountryEnum } from './CountryEnum';
import type { GenderEnum } from './GenderEnum';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type User = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly email?: string;
    readonly dateJoined?: string;
    gender?: GenderEnum;
    firstName?: string | null;
    lastName?: string | null;
    country?: CountryEnum;
    yearOfBirth?: number | null;
    favoriteVenue?: string;
    readonly isStaff?: boolean;
    readonly isAdmin?: boolean;
    /**
     * JWT access token, provides authentication for session-less requests when provided in header:
     * `Authorization: Bearer <token>`
     */
    readonly accessToken?: string;
    /**
     * CDN policy to be included when requesting protected media files from the CDN.
     * Expected cookie value: `Cloud-CDN-Cookie=<policy>; Path=/; Domain=<domain>; HttpOnly: SameSite=Lax`
     */
    readonly cdnPolicy?: string;
};

