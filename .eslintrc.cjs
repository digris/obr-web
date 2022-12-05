/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/eslint-config-typescript/recommended",
    "@vue/eslint-config-prettier",
  ],
  plugins: ["simple-import-sort", "import"],
  rules: {
    "arrow-body-style": "off",
    "no-shadow": "off",
    "no-unused-vars": "off",
    "import/prefer-default-export": "off", //
    "@typescript-eslint/no-shadow": ["error"],
    "@typescript-eslint/no-unused-vars": ["error"], //
    "vue/multi-word-component-names": "off", // transition
    "@typescript-eslint/ban-ts-comment": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-empty-function": "off", //
    "simple-import-sort/imports": "error",
    "simple-import-sort/exports": "error",
    "import/first": "error",
    "import/no-duplicates": "error" /*
    "vue/max-attributes-per-line": [
      "error",
      {
        singleline: {
          max: 1,
        },
        multiline: {
          max: 1,
        },
      },
    ],
    */,
    /*
        "vue/first-attribute-linebreak": [
          "error",
          {
            singleline: "ignore",
            multiline: "below",
          },
        ],
        */
    "vue/html-closing-bracket-newline": [
      "error",
      {
        singleline: "never",
        multiline: "always",
      },
    ],
    "vue/html-indent": [
      "error",
      2,
      {
        attribute: 1,
        baseIndent: 1,
        closeBracket: 0,
        alignAttributesVertically: true,
        ignores: [],
      },
    ],
  },
  overrides: [
    {
      // https://github.com/lydell/eslint-plugin-simple-import-sort#custom-grouping
      files: ["*.ts", "*.vue"],
      rules: {
        "simple-import-sort/imports": [
          "error",
          {
            groups: [
              ["^vue", "^@?\\w", "^pinia", "^lodash"],
              // ["^@/api"],
              // ["^@/stores"],
              // ["^@/composables"],
              // ["^@/components"],
              // ["^@?\\w"],
              ["^(@|components)(/.*|$)"],
              ["^"],
              ["^\\."],
              ["^.+\\.?(scss)$"],
            ],
          },
        ],
      },
    },
  ],
  env: {
    "vue/setup-compiler-macros": true,
  },
};
