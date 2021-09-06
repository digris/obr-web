/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Schedule = {
    properties: {
        key: {
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
        media: {
            type: 'ScheduleMedia',
            isRequired: true,
        },
        emission: {
            type: 'ScheduleEmission',
            isRequired: true,
        },
        playlist: {
            type: 'SchedulePlaylist',
            isRequired: true,
        },
    },
};