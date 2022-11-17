import { APIClient } from "@/api/client";
import { useAPIBaseUrl } from "@/composables/api";

const { APIBaseUrl } = useAPIBaseUrl();

const PAGE_ENDPOINT = `${APIBaseUrl.value}cms/page`;

async function getPage(path: string) {
  const url = `${PAGE_ENDPOINT}${path}`;
  const response = await APIClient.get(url);
  return response.data;
}

export { getPage };
