/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category } from './Category';

export type PaginatedCategoryList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Category>;
};

