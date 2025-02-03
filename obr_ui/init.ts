import { useAccount } from "@/composables/account";

const SSE_URL = "https://openbroadcast.ch/sse";

interface NewsItem {
  ts: number;
  cmd: "start" | "stop";
  provider: string;
}

export async function init(app) {
  console.log("init: start", app);

  const { settings } = useAccount();

  /******************************************************************
    event source is used to "consume" fast changing stats data
    ******************************************************************/
  const eventSource = new EventSource(`${SSE_URL}/news`);
  eventSource.onmessage = (event) => {
    const item: NewsItem = JSON.parse(event.data) as NewsItem;
    console.debug("sse", item);

    console.log("settings", settings);
    console.log("settings:newsProvider", settings.value.newsProvider);

    const { ts, cmd, provider } = item;

    const delay = (ts + 4) * 1000 - Date.now();
    // const delay = 0;

    console.debug("item", ts, cmd, provider, delay);
    if (cmd === "start") {
      console.debug("start", provider);

      if (settings.value.newsProvider !== provider) {
        console.debug("news provider not enabled", provider, settings.value.newsProvider);
        return;
      }

      setTimeout(() => {
        window.hlsPlayer.playNews(provider);
      }, delay);
    }

    if (cmd === "stop") {
      console.debug("stop");
      setTimeout(() => {
        window.hlsPlayer.endPlayNews();
      }, delay);
    }
  };
  console.log("init: end");
}
