import { APIClient } from '@/api/Client';
import settings from '@/settings';

const EDITOR_ENDPOINT = `${settings.API_BASE_URL}broadcast/editors/`;
const SCHEDULE_ENDPOINT = `${settings.API_BASE_URL}broadcast/schedule/`;

async function getSchedule(params: Object = {}) {
  const url = SCHEDULE_ENDPOINT;
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getEditors(limit: number, offset: number) {
  const url = EDITOR_ENDPOINT;
  const params = {
    limit, offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getEditor(uid: string) {
  const url = `${EDITOR_ENDPOINT}${uid}/`;
  const response = await APIClient.get(url);
  return response.data;
}

export {
  getSchedule,
  getEditors,
  getEditor,
};
