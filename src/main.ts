import './style/main.scss';
import createUIStateHandler from '@/utils/ui';
import createCredentialsHandler from '@/utils/credentials';
import createStationTimeHandler from '@/utils/time';
import creadeScheduleHandler from '@/broadcast/schedule';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

createStationTimeHandler();
createCredentialsHandler();
creadeScheduleHandler();
createUIStateHandler();

// console.debug('stateHandler', stateHandler);

createApp(App)
  .use(router)
  .use(store)
  .mount('#app');
