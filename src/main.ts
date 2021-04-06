import './style/main.scss';

// eslint-disable-next-line no-unused-vars
import UIStateHandler from '@/utils/ui';

import apolloClient from '@/graphql/client';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

// @ts-ignore
window.apolloClient = apolloClient;

createApp(App)
  .use(router)
  .use(store)
  .mount('#app');
