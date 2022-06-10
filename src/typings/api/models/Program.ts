/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProgramEmission } from './ProgramEmission';

export type Program = {
    timeFrom: string;
    timeUntil: string;
    emissions: Array<ProgramEmission>;
};

