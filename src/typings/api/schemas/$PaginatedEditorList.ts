/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $PaginatedEditorList = {
    properties: {
        count: {
            type: 'number',
        },
        next: {
            type: 'string',
            isNullable: true,
            format: 'uri',
        },
        previous: {
            type: 'string',
            isNullable: true,
            format: 'uri',
        },
        results: {
            type: 'array',
            contains: {
                type: 'Editor',
            },
        },
    },
};