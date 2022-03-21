// import applyConverters from 'axios-case-converter';
import axios from "axios";
import qs from "qs";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

// const APIClient = applyConverters(axios.create({
//   timeout: 5000,
//   headers: {
//     'X-Requested-With': 'XMLHttpRequest',
//   },
// }));

const APIClient = axios.create({
  timeout: 12000,
  headers: {
    "X-Requested-With": "XMLHttpRequest",
  },
});

const paramsSerializer = (params: any) => {
  return qs.stringify(params);
};

export { APIClient, paramsSerializer };
