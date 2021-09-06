/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Tag = {
    properties: {
        ct: {
            type: 'string',
            isReadOnly: true,
        },
        uid: {
            type: 'string',
            isReadOnly: true,
        },
        type: {
            type: 'TypeEnum',
        },
        name: {
            type: 'string',
            isRequired: true,
            maxLength: 100,
        },
    },
};