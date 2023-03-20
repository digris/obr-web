import axios from "axios";
import axiosRetry from "axios-retry";
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

APIClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // if (error.code > 499) {
    //   notify({
    //     level: "error",
    //     ttl: 5,
    //     body: `${error}`,
    //   });
    // }
    throw error;
  }
);

// NOTE: check for possible implications
axiosRetry(APIClient, {
  retries: 5,
  onRetry: (count, error) => {
    console.debug("retry", count, error);
  },
});

export { APIClient, paramsSerializer };
