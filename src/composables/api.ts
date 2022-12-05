import { computed } from "vue";
import { useStorage } from "@vueuse/core";

import settings from "@/settings";

const useAPIBaseUrl = () => {
  const locale = useStorage("settings/locale", "en");
  const prefix = computed(() => (locale.value === "en" ? "" : `/${locale.value}`));
  const APIBaseUrl = computed(() => {
    return `${prefix.value}${settings.API_BASE_URL}`;
  });
  return {
    APIBaseUrl,
  };
};

export { useAPIBaseUrl };
