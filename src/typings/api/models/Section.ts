/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Section = {
    /**
     * Content type
     */
    readonly ct: string;
    /**
     * UID
     */
    readonly uid: string;
    readonly title: string;
    readonly expandable: boolean;
    readonly body: string;
};

