/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { BlankEnum } from './BlankEnum';
import type { CountryEnum } from './CountryEnum';
import type { NullEnum } from './NullEnum';

export type PatchedAddressRequest = {
    line1?: string;
    line2?: string;
    postalCode?: string;
    city?: string;
    country?: (CountryEnum | BlankEnum | NullEnum) | null;
};

