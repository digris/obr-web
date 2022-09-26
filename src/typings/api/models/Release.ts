/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Release = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly url?: string;
    name: string;
    readonly numMedia?: number;
    readonly isNew?: boolean;
};

