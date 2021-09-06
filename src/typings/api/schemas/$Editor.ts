/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Editor = {
    properties: {
        url: {
            type: 'string',
            isReadOnly: true,
            format: 'uri',
        },
        ct: {
            type: 'string',
            isReadOnly: true,
        },
        uid: {
            type: 'string',
            isReadOnly: true,
        },
        name: {
            type: 'string',
            isRequired: true,
        },
    },
};