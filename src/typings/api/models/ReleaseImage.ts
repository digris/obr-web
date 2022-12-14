/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ReleaseImage = {
    /**
     * Content type
     */
    readonly ct?: string;
    /**
     * UID
     */
    readonly uid?: string;
    /**
     * To be used with `IMAGE_RESIZER_ENDPOINT`
     */
    readonly path?: string;
    /**
     * "Internal" storage backend URL
     */
    readonly url?: string;
    /**
     * Aspect ratio - e.g. `1.78` (16/9)
     */
    readonly ratio?: number;
    readonly rgb?: Array<number>;
};

