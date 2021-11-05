import { APIClient } from '@/api/client';
import settings from '@/settings';

const PAGE_ENDPOINT = `${settings.API_BASE_URL}cms/page`;

async function getPage(path: string) {
  const url = `${PAGE_ENDPOINT}${path}`;
  const response = await APIClient.get(url);
  return response.data;
}

export { getPage };
