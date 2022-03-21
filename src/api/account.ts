import { APIClient } from "@/api/client";
import settings from "@/settings";

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

async function loginByToken(email: string, token: string) {
  const url = `${ACCOUNT_ENDPOINT}token-login/`;
  const payload = {
    email,
    token,
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

async function getUser() {
  const url = `${ACCOUNT_ENDPOINT}users/me/?expand=settings,subscription,address`;
  const response = await APIClient.get(url);
  return response.data;
}

async function getSubscription() {
  const url = `${ACCOUNT_ENDPOINT}users/me/?fields=subscription&expand=subscription`;
  const response = await APIClient.get(url);
  return response.data?.subscription;
}

// async function refreshCredentials() {
//   const url = `${ACCOUNT_ENDPOINT}refresh-credentials/`;
//   const response = await APIClient.get(url);
//   return response.data;
// }

async function updateUser(payload: object) {
  const url = `${ACCOUNT_ENDPOINT}users/me/`;
  const response = await APIClient.patch(url, payload);
  return response.data;
}

async function updateAddress(payload: object) {
  const url = `${ACCOUNT_ENDPOINT}address/`;
  const response = await APIClient.patch(url, payload);
  return response.data;
}

async function updatePassword(password: string) {
  const url = `${ACCOUNT_ENDPOINT}password/`;
  const payload = {
    password,
  };
  const response = await APIClient.post(url, payload);
  return response.data?.subscription;
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
  loginByToken,
  loginBySignedEmail,
  getUser,
  getSubscription,
  // refreshCredentials,
  updateUser,
  updateAddress,
  updatePassword,
  getSocialBackends,
  disconnectSocialBackend,
};
