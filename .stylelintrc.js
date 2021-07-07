module.exports = {
  extends: [
    'stylelint-scss',
    'stylelint-config-recommended',
    'stylelint-config-rational-order',
  ],
  rules: {
    'at-rule-no-unknown': [true, {
      ignoreAtRules: ['debug', 'warn', 'function', 'if', 'else', 'use', 'each', 'include', 'extend', 'mixin', 'return', 'for'],
    }],
    indentation: 2,
    'color-hex-case': 'lower',
    'plugin/rational-order': [true, {
      'border-in-box-model': false,
      'empty-line-between-groups': false,
    }],
    'selector-pseudo-element-no-unknown': [true, {
      ignorePseudoElements: ["deep"],
    }],
    'selector-pseudo-class-no-unknown': [true, {
      ignorePseudoElements: ["deep"],
    }],
  },
};
