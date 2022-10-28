import { APIClient } from "@/api/client";
import { useAPIBaseUrl } from "@/composables/api";
const { APIBaseUrl } = useAPIBaseUrl();

const FAQ_ENDPOINT = `${APIBaseUrl.value}faq/categories/`;

async function getFaqCategories(limit = 100, offset = 0) {
  const url = FAQ_ENDPOINT;
  const params = {
    limit,
    offset,
  };
  const response = await APIClient.get(url, { params });
  return response.data;
}

export { getFaqCategories };
