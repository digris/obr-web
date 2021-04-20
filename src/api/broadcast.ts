import { APIClient } from '@/api/Client';
import settings from '@/settings';

const BROADCAST_ENDPOINT = `${settings.API_BASE_URL}broadcast/`;

async function getSchedule(params: Object = {}) {
  const url = `${BROADCAST_ENDPOINT}schedule/`;
  const response = await APIClient.get(url, { params });
  return response.data;
}

// eslint-disable-next-line import/prefer-default-export
export { getSchedule };
