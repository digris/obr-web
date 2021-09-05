/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Editor } from './Editor';

export type SchedulePlaylist = {
    readonly url?: string;
    readonly ct?: string;
    readonly uid?: string;
    name?: string | null;
    editor: Editor;
}
