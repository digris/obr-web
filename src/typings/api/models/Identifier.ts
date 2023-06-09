/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IdentifierScopeEnum } from './IdentifierScopeEnum';

export type Identifier = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  scope?: IdentifierScopeEnum | null;
  value?: string | null;
};

