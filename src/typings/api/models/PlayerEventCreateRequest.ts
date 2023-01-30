/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlayerEventCreateSourceEnum } from './PlayerEventCreateSourceEnum';
import type { StateEnum } from './StateEnum';

export type PlayerEventCreateRequest = {
    objKey: string;
    source: PlayerEventCreateSourceEnum;
    state: StateEnum;
    /**
     * Unix timestamp when event was created on the client.
     */
    ts: number;
};

