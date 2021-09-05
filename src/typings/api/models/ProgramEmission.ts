/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Editor } from './Editor';
import type { Tag } from './Tag';

export type ProgramEmission = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    playlistUid: string;
    name: string;
    series: Record<string, any> | null;
    editor: Editor;
    tags: Array<Tag>;
    readonly duration?: string;
    timeStart?: string | null;
    timeEnd?: string | null;
}
