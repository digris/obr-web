import './style/main.scss';
import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import * as Sentry from '@sentry/vue';
import { Integrations } from '@sentry/tracing';
import settings from '@/settings';
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
  .directive('tooltip', TooltipDirective);

Sentry.init({
  app,
  dsn: settings.SENTRY_DSN,
  integrations: [
    new Integrations.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracingOrigins: [
        'local.next.openbroadcast.ch',
        'next.openbroadcast.ch',
        'openbroadcast.ch',
        /^\//,
      ],
    }),
  ],
  tracesSampleRate: 1.0,
});

app.mount('#app');

// @ts-ignore
window.app = app;

// @ts-ignore
window.router = router;

// @ts-ignore
window.store = store;
