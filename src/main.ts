import "./style/main.scss";
import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import { createPinia } from "pinia";
import * as Sentry from "@sentry/vue";
import { Integrations } from "@sentry/tracing";
import OpenReplay from "@openreplay/tracker";
import trackerAxios from "@openreplay/tracker-axios";
import trackerAssist from "@openreplay/tracker-assist";
import settings from "@/settings";
import { useSettingsStore } from "@/stores/settings";
import createEventHandler from "@/stats/event";
import createUIStateHandler from "@/utils/ui";
import createStationTimeHandler from "@/utils/time";
import createAccountHandler from "@/utils/account";
import creadeScheduleHandler from "@/broadcast/schedule";
import createPlayerStateHandler from "@/player/handler";

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

const pinia = createPinia();

const app = createApp(App);
app.use(pinia);

const settingsStore = useSettingsStore();

// @ts-ignore
import de from "@/locales/de.yml";
// @ts-ignore
import en from "@/locales/en.yml";

const i18n = createI18n({
  legacy: false,
  locale: settingsStore.locale,
  fallbackLocale: "de",
  messages: {
    de,
    en,
  },
});

app.use(router);
app.use(store);
app.use(i18n);
app.directive("tooltip", TooltipDirective);

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

const tracker = new OpenReplay({
  projectKey: settings.OPENREPLAY_PROJECT_KEY,
  __DISABLE_SECURE_MODE: settings.DEBUG,
  onStart: ({ sessionToken }) => {
    Sentry.setTag("openReplaySessionToken", sessionToken);
  },
});
tracker.use(trackerAxios());
tracker.use(trackerAssist());
tracker.start().then(() => {});

// @ts-ignore
window.pinia = pinia;

// @ts-ignore
window.app = app;

// @ts-ignore
window.router = router;

// @ts-ignore
window.store = store;

// @ts-ignore
window.tracker = tracker;
