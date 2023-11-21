/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type SearchResultImage = {
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  /**
   * To be used with `IMAGE_RESIZER_ENDPOINT`
   */
  readonly path: string;
  /**
   * "Internal" storage backend URL
   */
  readonly url: string;
  readonly rgb: Array<number>;
};

