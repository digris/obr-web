/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EditorImage } from './EditorImage';

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type Editor = {
    /**
     * Content type
     */
    readonly ct: string;
    /**
     * UID
     */
    readonly uid: string;
    readonly url: string;
    readonly name: string;
    location?: string;
    description?: string;
    readonly role: string;
    readonly numPlaylists: number;
    readonly userRating: number | null;
    readonly image: EditorImage | null;
    isActive?: boolean;
};

