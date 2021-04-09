import './style/main.scss';

// eslint-disable-next-line no-unused-vars
import UIStateHandler from '@/utils/ui';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

createApp(App)
  .use(router)
  .use(store)
  .mount('#app');
