/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $MediaArtist = {
    properties: {
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
            isReadOnly: true,
        },
        joinPhrase: {
            type: 'string',
            isNullable: true,
            maxLength: 36,
        },
    },
};