import './style/main.scss';
import createUIStateHandler from '@/utils/ui';
import createCredentialsHandler from '@/utils/credentials';
import createStationTimeHandler from '@/utils/time';
import createAccountHandler from '@/utils/account';
import creadeScheduleHandler from '@/broadcast/schedule';

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';

// directives
// import { loginRequired } from './directives/account';
import { TooltipDirective } from './directives/tooltip';

createStationTimeHandler();
createCredentialsHandler();
creadeScheduleHandler();
createAccountHandler();
createUIStateHandler();

// console.debug('stateHandler', stateHandler);

createApp(App)
  .use(router)
  .use(store)
  .directive('tooltip', TooltipDirective)
  .mount('#app');
