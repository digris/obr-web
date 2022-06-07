import { APIClient } from "@/api/client";
import settings from "@/settings";

const STATS_ENDPOINT = `${settings.API_BASE_URL}stats/`;

async function createPlayerEvents(events: Array<object>) {
  const url = `${STATS_ENDPOINT}player-events/`;
  const payload = {
    events: [...events],
  };
  const response = await APIClient.put(url, payload);
  return response;
}

export { createPlayerEvents };
