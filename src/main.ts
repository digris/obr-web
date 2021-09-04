import './style/main.scss';
import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import createUIStateHandler from '@/utils/ui';
import createStationTimeHandler from '@/utils/time';
import createAccountHandler from '@/utils/account';
import creadeScheduleHandler from '@/broadcast/schedule';
import createPlayerStateHandler from '@/player/handler';
import messagesDE from '@/locales/de.json';

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

const i18n = createI18n({
  legacy: false,
  locale: 'de',
  messages: {
    de: messagesDE,
  },
});

const app = createApp(App)
  .use(i18n)
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
