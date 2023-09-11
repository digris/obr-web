import { APIClient } from "@/api/client";
import settings from "@/settings";

const STATS_ENDPOINT = `${settings.API_BASE_URL}stats/`;

async function createPlayerEvents(events: Array<object>) {
  const url = `${STATS_ENDPOINT}player-events/`;
  const payload = {
    events: [...events],
  };
  return await APIClient.put(url, payload);
}

async function sendHeartbeat(payload: object) {
  const url = `${STATS_ENDPOINT}heartbeat/`;
  return await APIClient.put(url, payload);
}

export { createPlayerEvents, sendHeartbeat };
