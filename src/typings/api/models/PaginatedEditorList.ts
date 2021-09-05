/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Editor } from './Editor';

export type PaginatedEditorList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Editor>;
}
