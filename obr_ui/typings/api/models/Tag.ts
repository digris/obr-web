/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TypeEnum } from './TypeEnum';

export type Tag = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  type?: TypeEnum;
  readonly name: string;
};

