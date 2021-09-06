/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ConnectedSocialBackendRequest = {
    properties: {
        provider: {
            type: 'string',
            isRequired: true,
            maxLength: 32,
        },
        uid: {
            type: 'string',
            isRequired: true,
            maxLength: 255,
        },
    },
};