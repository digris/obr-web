import applyConverters from 'axios-case-converter';
// import { Store } from 'vuex';
import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.withCredentials = true;

const APIClient = applyConverters(axios.create({
  // xsrfHeaderName: 'X-CSRFTOKEN',
  // xsrfCookieName: 'csrftoken',
  timeout: 5000,
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
}));

// eslint-disable-next-line import/prefer-default-export
export { APIClient };
