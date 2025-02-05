import { computed } from "vue";
import { storeToRefs } from "pinia";

import { updateSettings } from "@/api/account";
import { useAccount } from "@/composables/account";
import { usePlayerControls } from "@/composables/player";
import { useNewsStore } from "@/stores/news";

export const useNews = () => {
  const { settings: userSettings } = useAccount();
  const { playNews, endPlayNews } = usePlayerControls();
  const { schedule, provider: localProvider } = storeToRefs(useNewsStore());

  // use user settings in case of authenticated, else local storage
  const provider = computed({
    get: () => {
      return userSettings.value ? userSettings.value.newsProvider : localProvider.value;
    },
    set: async (value: string) => {
      if (userSettings.value) {
        userSettings.value.newsProvider = value;

        // persist to user settings
        try {
          await updateSettings(userSettings.value);
        } catch (e) {
          console.error(e);
        }
      } else {
        localProvider.value = value;
      }
    },
  });

  return {
    provider,
    localProvider,
    schedule,
    // exposed actions
    playNews,
    endPlayNews,
  };
};
