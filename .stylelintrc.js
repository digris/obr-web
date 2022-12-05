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
        'stylelint-config-prettier',
    ],
    rules: {
        'scss/double-slash-comment-whitespace-inside': 'always',
        'order/properties-order': ['top', 'position', 'height', 'width',],
        'selector-pseudo-class-no-unknown': [
          true,
          {
            ignorePseudoClasses: ['deep'],
          }
        ]
    },
    // customSyntax: 'postcss-html',
    ignoreFiles: ['**/*.tsx', '**/*.ts',],
}
