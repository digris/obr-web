import "./style/main.scss";
import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import * as Sentry from "@sentry/vue";
import { Integrations } from "@sentry/tracing";
import settings from "@/settings";
import { useLanguage } from "@/composables/language";
import createEventHandler from "@/stats/event";
import createUIStateHandler from "@/utils/ui";
import createStationTimeHandler from "@/utils/time";
import createAccountHandler from "@/utils/account";
import creadeScheduleHandler from "@/broadcast/schedule";
import createPlayerStateHandler from "@/player/handler";

// import messagesDE from "@/locales/de.json";
// import messagesEN from "@/locales/en.json";

import { messages } from "@/locales/messages";

import App from "./App.vue";
import store from "./store";
import router from "./router";

// directives
import { TooltipDirective } from "./directives/tooltip";

createEventHandler();
createStationTimeHandler();
creadeScheduleHandler();
createAccountHandler();
createUIStateHandler();
createPlayerStateHandler();

const { currentLanguage } = useLanguage();

const i18n = createI18n({
  legacy: true,
  locale: currentLanguage.value,
  messages: messages,
});

const app = createApp(App).use(i18n).use(router).use(store).directive("tooltip", TooltipDirective);

Sentry.init({
  app,
  dsn: settings.SENTRY_DSN,
  integrations: [
    new Integrations.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracingOrigins: ["local.obr-next", "next.openbroadcast.ch", "openbroadcast.ch", /^\//],
    }),
  ],
  tracesSampleRate: 1.0,
});

app.mount("#app");

// @ts-ignore
window.i18n = i18n;

// @ts-ignore
window.app = app;

// @ts-ignore
window.router = router;

// @ts-ignore
window.store = store;
