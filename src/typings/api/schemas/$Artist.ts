/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Artist = {
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
            maxLength: 256,
        },
        numMedia: {
            type: 'number',
            isRequired: true,
        },
        userRating: {
            type: 'number',
            isReadOnly: true,
            isNullable: true,
        },
    },
};