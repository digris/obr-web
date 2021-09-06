/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Emission = {
    properties: {
        url: {
            type: 'string',
            isReadOnly: true,
            format: 'uri',
        },
        playlist: {
            type: 'all-of',
            contains: [{
                type: 'EmissionPlaylist',
            }],
            isReadOnly: true,
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
        duration: {
            type: 'string',
            isReadOnly: true,
        },
        mediaSet: {
            type: 'array',
            contains: {
                type: 'EmissionMedia',
            },
            isRequired: true,
        },
    },
};