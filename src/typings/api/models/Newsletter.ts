/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Newsletter = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly title?: string;
    readonly description?: string;
    readonly isSubscribed?: boolean;
};

