import './style/main.scss';

import createUIStateHandler from '@/utils/ui';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

createUIStateHandler();

// console.debug('stateHandler', stateHandler);

createApp(App)
  .use(router)
  .use(store)
  .mount('#app');
