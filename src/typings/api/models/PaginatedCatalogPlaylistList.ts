/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CatalogPlaylist } from './CatalogPlaylist';

export type PaginatedCatalogPlaylistList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<CatalogPlaylist>;
}
