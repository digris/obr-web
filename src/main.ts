import { createApp } from "vue";
import { createI18n } from "vue-i18n";
// import { Integrations } from "@sentry/tracing";
// import * as Sentry from "@sentry/vue";
import log from "loglevel";
import { createPinia } from "pinia";

// @ts-ignore
import de from "@/locales/de.yml";
// @ts-ignore
import en from "@/locales/en.yml";
import createMediaSessionHandler from "@/proto/player/mediaSession";
// import settings from "@/settings";
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

// if (settings.SENTRY_DSN) {
//   Sentry.init({
//     app,
//     dsn: settings.SENTRY_DSN,
//     integrations: [
//       new Integrations.BrowserTracing({
//         routingInstrumentation: Sentry.vueRouterInstrumentation(router),
//         tracePropagationTargets: [
//           "local.obr-next",
//           "next.openbroadcast.ch",
//           "openbroadcast.ch",
//           /^\//,
//         ],
//       }),
//       new Sentry.Replay({
//         maskAllText: false,
//         blockAllMedia: false,
//       }),
//     ],
//     trackComponents: true,
//     tracesSampleRate: 1.0,
//     replaysSessionSampleRate: 0.1,
//     replaysOnErrorSampleRate: 1.0,
//   });
// }

// if (settings.SENTRY_DSN) {
//   Sentry.init({
//     app,
//     dsn: settings.SENTRY_DSN,
//   });
// }

app.mount("#app");

// @ts-ignore
window.pinia = pinia;

// @ts-ignore
window.app = app;

// @ts-ignore
window.router = router;

// @ts-ignore
// window.tracker = tracker;
