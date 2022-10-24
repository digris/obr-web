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
export type PatchedUserRequest = {
    gender?: GenderEnum;
    firstName?: string | null;
    lastName?: string | null;
    country?: CountryEnum;
    yearOfBirth?: number | null;
    favoriteVenue?: string;
};

