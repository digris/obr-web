/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type PlaylistEmission = {
    /**
     * Content type
     */
    readonly ct: string;
    /**
     * UID
     */
    readonly uid: string;
    readonly url: string;
    timeStart?: string | null;
    timeEnd?: string | null;
};

