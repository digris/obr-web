import applyConverters from 'axios-case-converter';
import axios from 'axios';

const APIClient = applyConverters(axios.create({
  xsrfHeaderName: 'X-CSRFTOKEN',
  xsrfCookieName: 'csrftoken',
  timeout: 5000,
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
}));

const initAPIClient = (store) => {
  APIClient.interceptors.request.use((config) => {
    store.commit('api/START_LOADING');
    return config;
  }, (error) => {
    store.commit('api/FINISH_LOADING');
    return Promise.reject(error);
  });

  APIClient.interceptors.response.use((response) => {
    store.commit('api/FINISH_LOADING');
    return response;
  }, (error) => {
    store.commit('api/FINISH_LOADING');
    return Promise.reject(error);
  });
};

export { APIClient, initAPIClient };
