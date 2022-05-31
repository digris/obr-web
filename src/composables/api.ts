import { computed } from "vue";
import settings from "@/settings";
import { useStorage } from "@vueuse/core";

const useAPIBaseUrl = () => {
  const locale = useStorage("settings/locale", "");
  const prefix = computed(() => (locale.value === "en" ? "" : `/${locale.value}`));
  const APIBaseUrl = computed(() => {
    return `${prefix.value}${settings.API_BASE_URL}`;
  });
  return {
    APIBaseUrl,
  };
};

export { useAPIBaseUrl };
