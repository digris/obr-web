import type { App } from "vue";

import { useNews } from "@/composables/news";
import type { NewsProvider } from "@/player/hlsPlayer";
import settings from "@/settings";

const SSE_PUBLISHER_URL = settings.SSE_PUBLISHER_URL;

interface NewsMessage {
  ts: number;
  cmd: "start" | "stop";
  provider: NewsProvider;
}

export async function init(app: App): Promise<void> {
  console.log("init", app);

  const { selectedProvider } = useNews();
  const { playNews, endPlayNews } = useNews();

  const sse = new EventSource(SSE_PUBLISHER_URL);

  sse.addEventListener("news", async (e): Promise<void> => {
    const message: NewsMessage = JSON.parse(e.data) as NewsMessage;

    console.info("SSE-event", message);

    const { ts, cmd, provider } = message;

    const delay = (ts + 4) * 1000 - Date.now();

    if (cmd === "start") {
      if (selectedProvider.value?.key !== provider) {
        console.info("news provider not enabled", selectedProvider);
        return;
      }

      setTimeout(async () => {
        await playNews(provider);
      }, delay);
    }

    if (cmd === "stop") {
      if (selectedProvider.value?.key !== provider) {
        console.info("news provider not enabled", selectedProvider);
        return;
      }

      setTimeout(async () => {
        await endPlayNews();
      }, delay);
    }
  });
}
