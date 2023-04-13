import { computed } from "vue";
import { useStorage } from "@vueuse/core";

import settings from "@/settings";

const useAPIBaseUrl = () => {
  const locale = useStorage("settings/locale", "en");
  const prefix = computed(() => (locale.value === "en" ? "" : `/${locale.value}`));
  const APIBaseUrl = computed(() => {
    /*
    NOTE: review behaviour:
          curl 'https://next.openbroadcast.ch/discover/playlists/' \
               -H 'accept-language: de,en-US;q=0.9,en;q=0.8'
    */
    /*
    if (settings.API_BASE_URL.substring(0, 4) == "/de/") {
      return settings.API_BASE_URL;
    }
    */
    return `${prefix.value}${settings.API_BASE_URL}`;
  });
  return {
    APIBaseUrl,
  };
};

export { useAPIBaseUrl };
