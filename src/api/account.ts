import { APIClient } from '@/api/Client';
import settings from '@/settings';

const ACCOUNT_ENDPOINT = `${settings.API_BASE_URL}account/`;

async function login(email: string, password: string) {
  const url = `${ACCOUNT_ENDPOINT}login/`;
  const payload = {
    email,
    password,
  };
  const response = await APIClient.post(url, payload);
  return response.data;
}

async function getCurrentUser() {
  const url = `${ACCOUNT_ENDPOINT}users/me/`;
  const response = await APIClient.get(url);
  return response.data;
}

export { login, getCurrentUser };
