import { APIClient } from "@/api/client";
import settings from "@/settings";
import type { UserVoucher } from "@/typings/api";

const SUBSCRIPTION_ENDPOINT = `${settings.API_BASE_URL}subscription/`;

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

async function redeemVoucher(code: string) {
  const url = `${SUBSCRIPTION_ENDPOINT}voucher/`;
  const payload = {
    code,
  };
  const response = await APIClient.post(url, payload);
  return response.data;
}

async function getUserVouchers(): Promise<Array<UserVoucher>> {
  const url = `${SUBSCRIPTION_ENDPOINT}user-vouchers/`;
  const response = await APIClient.get(url);
  return response.data;
}

export { createStripeCheckoutSession, getPlanOptions, getUserVouchers, getVoucher, redeemVoucher };
