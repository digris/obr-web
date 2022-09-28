/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

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
    firstName?: string | null;
    lastName?: string | null;
    readonly isStaff?: boolean;
    readonly isAdmin?: boolean;
    /**
     * JWT access token, provides authentication for session-less requests when provided in header:
     * `Authorization: Bearer <token>`
     */
    readonly accessToken?: string;
};

