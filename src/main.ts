import './style/main.scss';
import createUIStateHandler from '@/utils/ui';
import createStationTimeHandler from '@/utils/time';
import createAccountHandler from '@/utils/account';
import creadeScheduleHandler from '@/broadcast/schedule';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

// directives
import { TooltipDirective } from './directives/tooltip';

createStationTimeHandler();
creadeScheduleHandler();
createAccountHandler();
createUIStateHandler();

// console.debug('stateHandler', stateHandler);

createApp(App)
  .use(router)
  .use(store)
  .directive('tooltip', TooltipDirective)
  .mount('#app');

// @ts-ignore
window.router = router;

// @ts-ignore
window.store = store;
