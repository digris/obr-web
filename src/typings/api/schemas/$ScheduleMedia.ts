/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ScheduleMedia = {
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
        artistDisplay: {
            type: 'string',
            isReadOnly: true,
        },
        artists: {
            type: 'array',
            contains: {
                type: 'MediaArtist',
            },
            isReadOnly: true,
        },
        releases: {
            type: 'array',
            contains: {
                type: 'Release',
            },
            isReadOnly: true,
        },
    },
};