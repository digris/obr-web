/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CatalogPlaylist } from './CatalogPlaylist';
import type { Editor } from './Editor';
import type { Tag } from './Tag';

export type ProgramEmission = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly url?: string;
    readonly playlist?: CatalogPlaylist;
    readonly name?: string;
    readonly series?: Record<string, any> | null;
    readonly editor?: Editor | null;
    readonly tags?: Array<Tag> | null;
    readonly duration?: string;
    timeStart?: string | null;
    timeEnd?: string | null;
};

