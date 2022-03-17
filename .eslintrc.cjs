/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  "root": true,
  "extends": [
    "plugin:vue/vue3-essential",
    // ported from previous webpack setup
    // '@vue/airbnb',
    // '@vue/typescript',
    // below the vue3 suggested ones
    "eslint:recommended",
    "@vue/eslint-config-typescript/recommended",
    "@vue/eslint-config-prettier"
  ],
  "rules": {
    // ignores during transition to vite
    "vue/multi-word-component-names": "off",
    "@typescript-eslint/ban-ts-comment": "off",
    //
    "arrow-body-style": "off",
    "no-shadow": "off",
    "import/prefer-default-export": "off",
    "@typescript-eslint/no-shadow": [
      "error"
    ],
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": [
      "error"
    ],
    // "vue/max-attributes-per-line": [
    //   "error",
    //   {
    //     "singleline": {
    //       "max": 1,
    //       "allowFirstLine": false
    //     },
    //     "multiline": {
    //       "max": 1,
    //       "allowFirstLine": false
    //     }
    //   }
    // ],
    "vue/html-closing-bracket-newline": [
      "error",
      {
        "singleline": "never",
        "multiline": "always"
      }
    ],
    "vue/html-indent": [
      "error",
      2,
      {
        "attribute": 1,
        "baseIndent": 1,
        "closeBracket": 0,
        "alignAttributesVertically": true,
        "ignores": []
      }
    ]
  },
  "env": {
    "vue/setup-compiler-macros": true
  },
  "overrides": [
    {
      "files": [
        "cypress/integration/**.spec.{js,ts,jsx,tsx}"
      ],
      "extends": [
        "plugin:cypress/recommended"
      ]
    }
  ]
}
