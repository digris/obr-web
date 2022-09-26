/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Image } from './Image';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Editor = {
    readonly url?: string;
    readonly ct?: string;
    /**
     * UID
     */
    uid: string;
    /**
     * me the help text
     */
    name: string;
    location?: string;
    description?: string;
    readonly role?: string;
    readonly numPlaylists?: number;
    readonly userRating?: number | null;
    readonly image?: Image | null;
    isActive?: boolean;
};

