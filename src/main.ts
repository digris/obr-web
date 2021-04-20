import './style/main.scss';

import createUIStateHandler from '@/utils/ui';
import creadeScheduleHandler from '@/broadcast/schedule';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

creadeScheduleHandler();
createUIStateHandler();

// console.debug('stateHandler', stateHandler);

createApp(App)
  .use(router)
  .use(store)
  .mount('#app');
