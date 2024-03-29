module.exports = {
    // root: true,
    plugins: [
      'stylelint-order',
      'stylelint-scss',
    ],
    extends: [
        'stylelint-config-standard',
        'stylelint-config-standard-scss',
        'stylelint-config-recommended-vue',
        'stylelint-config-recommended-vue/scss',
    ],
    rules: {
        'declaration-block-no-redundant-longhand-properties': [
          true,
          {
            ignoreShorthands: ['grid-gap'],
          }
        ],
        'selector-pseudo-class-no-unknown': [
          true,
          {
            ignorePseudoClasses: ['deep'],
          }
        ],
        'scss/double-slash-comment-whitespace-inside': 'always',
        'order/properties-order': ['top', 'position', 'height', 'width',],
        'color-function-notation': 'modern',
    },
    // customSyntax: 'postcss-html',
    ignoreFiles: [
      '**/*.tsx',
      '**/*.ts',
      'obr_ui/views/proto/**.*',
    ],
}
