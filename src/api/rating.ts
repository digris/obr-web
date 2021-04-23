import { APIClient } from '@/api/Client';
import settings from '@/settings';

const VOTE_ENDPOINT = `${settings.API_BASE_URL}rating/`;

async function getRating(key: string) {
  const url = `${VOTE_ENDPOINT}${key}/`;
  const response = await APIClient.get(url);
  return response.data;
}

// eslint-disable-next-line import/prefer-default-export
export { getRating };
