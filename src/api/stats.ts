import { APIClient } from "@/api/client";
import settings from "@/settings";

const STATS_ENDPOINT = `${settings.API_BASE_URL}stats/`;

async function createPlayerEvents(events: Array<object>) {
  const url = `${STATS_ENDPOINT}player-events/`;
  const payload = {
    events: [...events],
  };
  const response = await APIClient.put(url, payload);
  console.debug("response", response);
  return response;
}

export { createPlayerEvents };
