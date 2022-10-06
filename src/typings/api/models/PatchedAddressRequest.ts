/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CountryEnum } from './CountryEnum';

export type PatchedAddressRequest = {
    line1?: string;
    line2?: string;
    postalCode?: string;
    city?: string;
    country?: CountryEnum;
};

