/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $EmissionMedia = {
    properties: {
        uid: {
            type: 'string',
            isRequired: true,
        },
        cueIn: {
            type: 'number',
            isRequired: true,
        },
        cueOut: {
            type: 'number',
            isRequired: true,
        },
        fadeIn: {
            type: 'number',
            isRequired: true,
        },
        fadeOut: {
            type: 'number',
            isRequired: true,
        },
        fadeCross: {
            type: 'number',
            isRequired: true,
        },
        timeStart: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        timeEnd: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
    },
};