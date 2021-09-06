/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Program = {
    properties: {
        timeFrom: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        timeUntil: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        emissions: {
            type: 'array',
            contains: {
                type: 'ProgramEmission',
            },
            isRequired: true,
        },
    },
};