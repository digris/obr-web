import qs from "qs";
import axios from "axios";
import axiosRetry from "axios-retry";

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
  timeout: 20000,
  headers: {
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "",
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
  retries: 10,
  retryCondition: (e) => {
    // extend default behavior to include 429
    return e.response?.status === 429 || axiosRetry.isNetworkOrIdempotentRequestError(e);
  },
  retryDelay: (count, e) => {
    // handle rate limit
    if (e.response?.status === 429) {
      const retryAfter = e.response.headers["retry-after"];
      if (Number.isInteger(parseInt(retryAfter))) {
        return parseInt(retryAfter) * 1000 + 1000;
      }
    }
    // built-in back-off delay
    return axiosRetry.exponentialDelay(count);
  },
});

export { APIClient, paramsSerializer };
