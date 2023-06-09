/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProgramEmission } from './ProgramEmission';

export type Program = {
  readonly timeFrom: string;
  readonly timeUntil: string;
  readonly emissions: Array<ProgramEmission>;
};

