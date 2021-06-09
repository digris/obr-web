/*
 check to use rules from here:
 https://gist.github.com/nkbt/9efd4facb391edbf8048
 */
module.exports = {
  root: true,

  env: {
    node: true,
    es6: true,
  },

  parserOptions: {
    parser: '@typescript-eslint/parser',
  },

  rules: {
    'arrow-body-style': 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
  },

  plugins: [
    'vue',
  ],

  extends: [
    'plugin:vue/vue3-essential',
    '@vue/airbnb',
    '@vue/typescript',
  ],
};
