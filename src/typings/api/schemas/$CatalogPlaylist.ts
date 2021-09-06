/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $CatalogPlaylist = {
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
        series: {
            type: 'string',
            isReadOnly: true,
        },
        latestEmission: {
            type: 'string',
            isReadOnly: true,
            format: 'date-time',
        },
        numMedia: {
            type: 'number',
            isReadOnly: true,
        },
        numEmissions: {
            type: 'number',
            isReadOnly: true,
        },
        userRating: {
            type: 'number',
            isReadOnly: true,
            isNullable: true,
        },
    },
};