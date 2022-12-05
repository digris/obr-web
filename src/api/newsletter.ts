import { APIClient } from "@/api/client";
import { useAPIBaseUrl } from "@/composables/api";

const { APIBaseUrl } = useAPIBaseUrl();

const NEWSLETTER_ENDPOINT = `${APIBaseUrl.value}newsletter/`;

export async function getNewsletters() {
  const url = `${NEWSLETTER_ENDPOINT}newsletters/`;
  const response = await APIClient.get(url);
  return response.data;
}

export async function updateSubscriptions(subscriptions: string[] = []) {
  const url = `${NEWSLETTER_ENDPOINT}newsletters/`;
  const payload = {
    newsletterUids: subscriptions,
  };
  const response = await APIClient.post(url, payload);
  return response.data;
}
