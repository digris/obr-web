/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type PlayerEvent = {
    time: string;
    state: string;
    objKey: string;
    source: string;
    userIdentity: string;
    deviceKey: string;
    ingested?: boolean;
};
