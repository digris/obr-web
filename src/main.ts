import { createApp } from "vue";
import { createI18n } from "vue-i18n";
// import OpenReplay from "@openreplay/tracker";
// import trackerAssist from "@openreplay/tracker-assist";
// import trackerAxios from "@openreplay/tracker-axios";
import { Integrations } from "@sentry/tracing";
import * as Sentry from "@sentry/vue";
import log from "loglevel";
import { createPinia } from "pinia";

// import { APIClient } from "@/api/client";
// @ts-ignore
import de from "@/locales/de.yml";
// @ts-ignore
import en from "@/locales/en.yml";
import createMediaSessionHandler from "@/player/mediaSession";
import settings from "@/settings";
import createEventHandler from "@/stats/event";
import { useSettingsStore } from "@/stores/settings";
import createAccountHandler from "@/utils/account";
import createScheduleHandler from "@/utils/schedule";
import setDocumentTheme from "@/utils/theme";
import createUIStateHandler from "@/utils/ui";

import App from "./App.vue";
// directives
import { TooltipDirective } from "./directives/tooltip";
import router from "./router";

import "./style/main.scss";

log.setLevel("TRACE");

const pinia = createPinia();

const app = createApp(App);
app.use(pinia);

const settingsStore = useSettingsStore();

setDocumentTheme();

createEventHandler();
createScheduleHandler();
createAccountHandler();
createUIStateHandler();
createMediaSessionHandler();

// import { numberFormats } from "@/locales/formats";

const i18n = createI18n({
  legacy: false,
  locale: settingsStore.locale,
  fallbackLocale: "de",
  globalInjection: false,
  messages: {
    de,
    en,
  },
  // numberFormats,
});

app.use(router);
app.use(i18n);
app.directive("tooltip", TooltipDirective);

// declare global {
//   interface Window {
//     tracker: OpenReplay;
//   }
// }

if (settings.SENTRY_DSN) {
  Sentry.init({
    app,
    dsn: settings.SENTRY_DSN,
    integrations: [
      new Integrations.BrowserTracing({
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
        tracePropagationTargets: [
          "local.obr-next",
          "next.openbroadcast.ch",
          "openbroadcast.ch",
          /^\//,
        ],
      }),
      new Sentry.Replay({
        maskAllText: true,
        blockAllMedia: true,
      }),
    ],
    trackComponents: true,
    tracesSampleRate: 1.0,
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
  });
}

/*
let tracker = null;
if (settings.OPENREPLAY_PROJECT_KEY) {
  tracker = new OpenReplay({
    projectKey: settings.OPENREPLAY_PROJECT_KEY,
    __DISABLE_SECURE_MODE: settings.DEBUG,
    onStart: ({ sessionToken }) => {
      Sentry.setTag("openReplaySessionToken", sessionToken);
    },
  });
  tracker.use(
    trackerAxios({
      instance: APIClient,
    })
  );
  tracker.use(trackerAssist());
  tracker.start().then(() => {});
}
*/

app.mount("#app");

// @ts-ignore
window.pinia = pinia;

// @ts-ignore
window.app = app;

// @ts-ignore
window.router = router;

// @ts-ignore
// window.tracker = tracker;
