/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CatalogPlaylist } from './CatalogPlaylist';
import type { Editor } from './Editor';
import type { Tag } from './Tag';

export type ProgramEmission = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    playlist: CatalogPlaylist;
    name: string;
    series: Record<string, any> | null;
    editor: Editor | null;
    tags: Array<Tag> | null;
    readonly duration?: string;
    timeStart?: string | null;
    timeEnd?: string | null;
};

