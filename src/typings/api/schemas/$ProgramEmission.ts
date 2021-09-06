/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProgramEmission = {
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
        playlistUid: {
            type: 'string',
            isRequired: true,
        },
        name: {
            type: 'string',
            isRequired: true,
        },
        series: {
            type: 'dictionary',
            contains: {
                properties: {
                },
            },
            isRequired: true,
            isNullable: true,
        },
        editor: {
            type: 'Editor',
            isRequired: true,
        },
        tags: {
            type: 'array',
            contains: {
                type: 'Tag',
            },
            isRequired: true,
        },
        duration: {
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