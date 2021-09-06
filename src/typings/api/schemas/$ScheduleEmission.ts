/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ScheduleEmission = {
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
        timeStart: {
            type: 'string',
            isNullable: true,
            format: 'date-time',
        },
        timeEnd: {
            type: 'string',
            isNullable: true,
            format: 'date-time',
        },
    },
};