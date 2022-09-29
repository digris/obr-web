/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type PatchedUserRequest = {
    firstName?: string | null;
    lastName?: string | null;
};
