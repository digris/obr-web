// import applyConverters from 'axios-case-converter';
import axios from "axios";
import qs from "qs";
import notify from "@/utils/notification";

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

APIClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // console.debug('EC', error.code);
    if (error.code > 499) {
      notify({
        level: "error",
        ttl: 5,
        body: `${error}`,
      });
    }
    throw error;
  }
);

export { APIClient, paramsSerializer };
