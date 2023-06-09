/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * A ModelSerializer that takes additional arguments for
 * "fields", "omit" and "expand" in order to
 * control which fields are displayed, and whether to replace simple
 * values with complex, nested serializations
 */
export type PlayoutScheduleMedia = {
  readonly url: string;
  /**
   * Content type
   */
  readonly ct: string;
  /**
   * UID
   */
  readonly uid: string;
  readonly name: string;
  /**
   * in milliseconds
   */
  readonly duration: number;
};

