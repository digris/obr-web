import { APIClient } from "@/api/client";
import settings from "@/settings";

const SCHEDULE_ENDPOINT = `${settings.API_BASE_URL}broadcast/schedule/`;
const PROGRAM_ENDPOINT = `${settings.API_BASE_URL}broadcast/program/`;
const EDITOR_ENDPOINT = `${settings.API_BASE_URL}broadcast/editors/`;
const EMISSION_ENDPOINT = `${settings.API_BASE_URL}broadcast/emissions/`;

async function getSchedule(params: any) {
  const response = await APIClient.get(SCHEDULE_ENDPOINT, { params });
  return response.data;
}

async function getProgram(date: string) {
  const url = PROGRAM_ENDPOINT;
  const params = {
    date,
  };
  const response = await APIClient.get(url, { params });
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
  const params = {
    expand: ["identifiers"],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

async function getEmission(uid: string) {
  const url = `${EMISSION_ENDPOINT}${uid}/`;
  const params = {
    expand: ["media_set"],
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export { getSchedule, getProgram, getEditors, getEditor, getEmission };
