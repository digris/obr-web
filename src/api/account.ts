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

async function logout() {
  const url = `${ACCOUNT_ENDPOINT}logout/`;
  const response = await APIClient.post(url);
  return response.data;
}

async function checkLoginEmail(email: string) {
  const url = `${ACCOUNT_ENDPOINT}send-email-login/?email=${email}`;
  const response = await APIClient.get(url);
  return response.data;
}

async function sendLoginEmail(email: string) {
  const url = `${ACCOUNT_ENDPOINT}send-email-login/`;
  const payload = {
    email,
  };
  const response = await APIClient.post(url, payload);
  return response.data;
}

async function loginBySignedEmail(signedEmail: string) {
  const url = `${ACCOUNT_ENDPOINT}signed-email-login/`;
  const payload = {
    signedEmail,
  };
  const response = await APIClient.post(url, payload);
  return response.data;
}

async function getCurrentUser() {
  const url = `${ACCOUNT_ENDPOINT}users/me/?expand=settings,subscription`;
  const response = await APIClient.get(url);
  return response.data;
}

async function refreshCredentials() {
  const url = `${ACCOUNT_ENDPOINT}refresh-credentials/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function getSocialBackends() {
  const url = `${ACCOUNT_ENDPOINT}social-backends/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function disconnectSocialBackend(provider: string, uid: string) {
  const url = `${ACCOUNT_ENDPOINT}social-backends/${provider}/${uid}/`;
  const response = await APIClient.delete(url);
  return response.data;
}

export {
  login,
  logout,
  checkLoginEmail,
  sendLoginEmail,
  loginBySignedEmail,
  getCurrentUser,
  refreshCredentials,
  getSocialBackends,
  disconnectSocialBackend,
};
