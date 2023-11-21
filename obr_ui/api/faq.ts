import { APIClient } from "@/api/client";
import { useAPIBaseUrl } from "@/composables/api";
import type { Category } from "@/typings/api";

const { APIBaseUrl } = useAPIBaseUrl();

const FAQ_ENDPOINT = `${APIBaseUrl.value}faq/categories/`;

interface CategoryListResponse {
  results: Array<Category>;
}

async function getFaqCategories(limit = 100, offset = 0) {
  const url = FAQ_ENDPOINT;
  const params = {
    limit,
    offset,
  };
  const response = await APIClient.get<CategoryListResponse>(url, { params });
  return response.data.results;
}

export { Category as FaqCategory, getFaqCategories };
