/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Voucher = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    readonly code?: string;
    readonly codeDisplay?: string;
    numDays?: number;
    readonly isValid?: boolean;
    readonly isValidForUser?: boolean;
    readonly untilDate?: string | null;
    validUntil?: string;
};

