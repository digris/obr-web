import './style/main.scss';
import { createApp } from 'vue';
import createUIStateHandler from '@/utils/ui';
import createStationTimeHandler from '@/utils/time';
import createAccountHandler from '@/utils/account';
import creadeScheduleHandler from '@/broadcast/schedule';
import createPlayerStateHandler from '@/player/handler';

import App from './App.vue';
import store from './store';
import router from './router';

// directives
import { TooltipDirective } from './directives/tooltip';

createStationTimeHandler();
creadeScheduleHandler();
createAccountHandler();
createUIStateHandler();
createPlayerStateHandler();

// console.debug('stateHandler', stateHandler);

const app = createApp(App)
  .use(router)
  .use(store)
  .directive('tooltip', TooltipDirective)
  .mount('#app');

// @ts-ignore
window.app = app;

// @ts-ignore
window.router = router;

// @ts-ignore
window.store = store;
