import { APIClient } from "@/api/client";
import settings from "@/settings";

const VOTE_ENDPOINT = `${settings.API_BASE_URL}rating/`;

async function getRating(key: string) {
  const url = `${VOTE_ENDPOINT}${key}/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function postRating(key: string, value: number | null) {
  const url = `${VOTE_ENDPOINT}${key}/`;
  const payload = { value };
  const response = await APIClient.post(url, payload);
  return response.data;
}

export { getRating, postRating };
