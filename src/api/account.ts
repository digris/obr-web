import { APIClient } from "@/api/client";
import { useAPIBaseUrl } from "@/composables/api";

const { APIBaseUrl } = useAPIBaseUrl();

// const ACCOUNT_ENDPOINT = `${settings.API_BASE_URL}account/`;
const ACCOUNT_ENDPOINT = `${APIBaseUrl.value}account/`;

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
  const url = `${ACCOUNT_ENDPOINT}send-email-login/?email=${encodeURIComponent(email)}`;
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

async function getSignedLoginCredentials() {
  const url = `${ACCOUNT_ENDPOINT}signed-login-credentials/`;
  const response = await APIClient.post(url);
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

async function updateUser(payload: any) {
  const url = `${ACCOUNT_ENDPOINT}users/me/`;
  const response = await APIClient.patch(url, payload);
  return response.data;
}

async function updateAddress(payload: any) {
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

async function getAddressCountries() {
  const url = `${ACCOUNT_ENDPOINT}address-countries/`;
  const response = await APIClient.get(url);
  return response.data;
}

export {
  checkLoginEmail,
  disconnectSocialBackend,
  //
  getAddressCountries,
  getSignedLoginCredentials,
  getSocialBackends,
  getSubscription,
  getUser,
  login,
  loginBySignedEmail,
  loginByToken,
  logout,
  sendLoginEmail,
  updateAddress,
  updatePassword,
  // refreshCredentials,
  updateUser,
};
