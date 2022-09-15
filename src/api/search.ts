import { APIClient } from "@/api/client";
import settings from "@/settings";

const SEARCH_ENDPOINT = `${settings.API_BASE_URL}search/`;

async function getGlobalSearchResults(q: string) {
  const url = `${SEARCH_ENDPOINT}global/`;
  const params = {
    q,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export { getGlobalSearchResults };
