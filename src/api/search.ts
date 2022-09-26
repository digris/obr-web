import { APIClient } from "@/api/client";
import settings from "@/settings";

const SEARCH_ENDPOINT = `${settings.API_BASE_URL}search/`;

async function getGlobalMediaSearchResults(q: string, limit = 100) {
  const url = `${SEARCH_ENDPOINT}global/media/`;
  const params = {
    q,
    limit,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export { getGlobalMediaSearchResults };
