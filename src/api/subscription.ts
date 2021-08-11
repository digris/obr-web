import { APIClient } from '@/api/Client';
import settings from '@/settings';

const SUBSCRIPTION_ENDPOINT = `${settings.API_BASE_URL}subscription/`;

async function getCurrentSubscription() {
  const response = await APIClient.get(SUBSCRIPTION_ENDPOINT);
  return response.data;
}

async function getTrialOptions() {
  const url = `${SUBSCRIPTION_ENDPOINT}trial/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function startTrial() {
  const url = `${SUBSCRIPTION_ENDPOINT}trial/`;
  const response = await APIClient.put(url);
  return response.data;
}

async function getPlanOptions() {
  const url = `${SUBSCRIPTION_ENDPOINT}plan/`;
  const response = await APIClient.get(url);
  return response.data;
}

async function createStripeCheckoutSession(sku: string, next: string) {
  const url = `${SUBSCRIPTION_ENDPOINT}payment/stripe/`;
  const payload = {
    sku,
    next,
  };
  const response = await APIClient.post(url, payload);
  return response.data;
}

async function getVoucher(code: string) {
  const url = `${SUBSCRIPTION_ENDPOINT}voucher/`;
  const params = {
    code,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export {
  getCurrentSubscription,
  getTrialOptions,
  startTrial,
  getPlanOptions,
  // payment
  createStripeCheckoutSession,
  // voucher
  getVoucher,
};
