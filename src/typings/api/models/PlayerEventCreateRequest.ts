/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SourceEnum } from './SourceEnum';
import type { StateEnum } from './StateEnum';

export type PlayerEventCreateRequest = {
    objKey: string;
    source: SourceEnum;
    state: StateEnum;
    /**
     * Unix timestamp when event was created on the client.
     */
    ts: number;
};

