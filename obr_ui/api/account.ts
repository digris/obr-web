import { APIClient } from "@/api/client";
import { useAPIBaseUrl } from "@/composables/api";
import type { AddressCountries } from "@/typings";

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
  // NOTE: maybe we should return the same data for
  //       all login requests.
  return {
    created: response.status === 201,
    user: response.data,
  };
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

async function loginByAppleId(idToken: string, authorizationCode: string, profile: object) {
  const url = `${ACCOUNT_ENDPOINT}apple-id-login/`;
  const payload = {
    idToken,
    authorizationCode,
    profile,
  };
  const response = await APIClient.post(url, payload);
  // NOTE: maybe we should return the same data for
  //       all login requests.
  return {
    created: response.status === 201,
    user: response.data,
  };
}

async function loginByGoogleIdToken(idToken: string) {
  const url = `${ACCOUNT_ENDPOINT}google-id-token-login/`;
  const payload = {
    idToken,
  };
  const response = await APIClient.post(url, payload);
  // NOTE: maybe we should return the same data for
  //       all login requests.
  return {
    created: response.status === 201,
    user: response.data,
  };
}

async function loginByGoogleOneTap(credential: string) {
  const url = `${ACCOUNT_ENDPOINT}google-one-tap-login/`;
  const payload = {
    credential,
  };
  const response = await APIClient.post(url, payload);
  // NOTE: maybe we should return the same data for
  //       all login requests.
  return {
    created: response.status === 201,
    user: response.data,
  };
}

async function getUser() {
  const url = `${ACCOUNT_ENDPOINT}users/me/?expand=settings,subscription,address,recurring_donation`;
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

async function updateEmail(email: string) {
  const url = `${ACCOUNT_ENDPOINT}email/`;
  const payload = {
    email,
  };
  const response = await APIClient.post(url, payload);
  return response.data?.subscription;
}

async function updatePassword(password: string) {
  const url = `${ACCOUNT_ENDPOINT}password/`;
  const payload = {
    password,
  };
  const response = await APIClient.post(url, payload);
  return response.data?.subscription;
}

async function updateAddress(payload: any) {
  const url = `${ACCOUNT_ENDPOINT}address/`;
  const response = await APIClient.patch(url, payload);
  return response.data;
}

async function updateSettings(payload: any) {
  const url = `${ACCOUNT_ENDPOINT}settings/`;
  const response = await APIClient.patch(url, payload);
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

async function getAddressCountries() {
  const url = `${ACCOUNT_ENDPOINT}address-countries/`;
  const response = await APIClient.get<AddressCountries[]>(url);
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
  loginByAppleId,
  loginByGoogleIdToken,
  loginByGoogleOneTap,
  loginBySignedEmail,
  loginByToken,
  logout,
  sendLoginEmail,
  updateAddress,
  updateEmail,
  updatePassword,
  updateSettings,
  // refreshCredentials,
  updateUser,
};
