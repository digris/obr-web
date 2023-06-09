/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type StreamEventRequest = {
    ip?: string | null;
    path?: string;
    method?: string;
    status?: number;
    bytesSent?: number;
    referer: string;
    userAgent?: string;
    secondsConnected?: number;
    timeStart: string;
    timeEnd: string;
};

