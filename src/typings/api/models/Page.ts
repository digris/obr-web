/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Section } from './Section';

export type Page = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  readonly title: string;
  readonly lead: string;
  readonly sections: Array<Section>;
};

