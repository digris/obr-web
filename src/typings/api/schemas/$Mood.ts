/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Mood = {
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
            maxLength: 36,
        },
        teaser: {
            type: 'string',
            isNullable: true,
            maxLength: 256,
        },
    },
};