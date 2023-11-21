/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Topic } from './Topic';

export type Category = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  readonly name: string;
  readonly topics: Array<Topic>;
};

