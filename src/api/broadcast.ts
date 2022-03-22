import { APIClient } from "@/api/client";
import settings from "@/settings";

const SCHEDULE_ENDPOINT = `${settings.API_BASE_URL}broadcast/schedule/`;
const PROGRAM_ENDPOINT = `${settings.API_BASE_URL}broadcast/program/`;
const EDITOR_ENDPOINT = `${settings.API_BASE_URL}broadcast/editors/`;

async function getSchedule(params: Object = {}) {
  const response = await APIClient.get(SCHEDULE_ENDPOINT, { params });
  return response.data;
}

async function getProgram() {
  const response = await APIClient.get(PROGRAM_ENDPOINT);
  return response.data;
}

async function getEditors(limit: number, offset: number) {
  const url = EDITOR_ENDPOINT;
  const params = {
    limit,
    offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getEditor(uid: string) {
  const url = `${EDITOR_ENDPOINT}${uid}/`;
  const response = await APIClient.get(url);
  return response.data;
}

export { getSchedule, getProgram, getEditors, getEditor };
