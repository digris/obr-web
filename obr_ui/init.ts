import type { App } from "vue";
import type { AxiosError } from "axios";

import { loginByGoogleOneTap } from "@/api/account";
import { useAccount } from "@/composables/account";
import { useNews } from "@/composables/news";
import { useNotification } from "@/composables/notification";
import type { NewsProvider } from "@/player/hlsPlayer";
import settings from "@/settings";

const SSE_PUBLISHER_URL = settings.SSE_PUBLISHER_URL;
const GOOGLE_AUTH_CLIENT_ID = settings.GOOGLE_AUTH_CLIENT_ID;

interface NewsMessage {
  ts: number;
  cmd: "start" | "stop";
  provider: NewsProvider;
}

export async function init(app: App): Promise<void> {
  /*
  NOTE: we run some random init steps here. likely this should be
  refactored at some point of time
  */

  console.debug("init", app);

  /*
  NOTE: SSE-handler (news)
  */
  const { selectedProvider } = useNews();
  const { playNews, endPlayNews } = useNews();

  const sse = new EventSource(SSE_PUBLISHER_URL);

  sse.addEventListener("news", async (e): Promise<void> => {
    const message: NewsMessage = JSON.parse(e.data) as NewsMessage;

    console.debug("SSE-event", message);

    const { ts, cmd, provider } = message;

    const delay = (ts + 4) * 1000 - Date.now();

    if (cmd === "start") {
      if (selectedProvider.value?.key !== provider) {
        return;
      }

      setTimeout(async () => {
        await playNews(provider);
      }, delay);
    }

    if (cmd === "stop") {
      if (selectedProvider.value?.key !== provider) {
        return;
      }

      setTimeout(async () => {
        await endPlayNews();
      }, delay);
    }
  });

  /*
  NOTE: google one-tap sign-in
  */
  window.onload = async function () {
    if (settings.CLIENT_MODE === "web" && google?.accounts) {
      const { loadUser, user } = useAccount();
      const { notify } = useNotification();

      google.accounts.id.initialize({
        client_id: GOOGLE_AUTH_CLIENT_ID,
        auto_select: true,
        cancel_on_tap_outside: false,
        context: "use",
        callback: async (response: object) => {
          try {
            await loginByGoogleOneTap(response.credential);
            await loadUser();
            await notify({
              level: "success",
              body: `logged in as ${user.value?.email}`,
              ttl: 3,
            });
          } catch (err: unknown) {
            const error = err as AxiosError;
            const message = error.response?.data.message ?? "Login error";
            await notify({
              level: "error",
              body: `login error: ${message}`,
              ttl: 30,
            });
          }
        },
      });

      console.debug("current user", user.value);
      if (!user.value) {
        google.accounts.id.prompt();
      }
    }
  };
}
