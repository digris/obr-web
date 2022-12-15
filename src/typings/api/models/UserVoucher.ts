/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserVoucher = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly codeDisplay?: string;
    readonly isValid?: boolean;
    readonly validUntil?: string;
    readonly numDays?: number;
    readonly numUsed?: number;
};

