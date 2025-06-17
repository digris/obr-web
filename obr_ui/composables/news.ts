import { type WritableComputedRef, computed } from "vue";
import { storeToRefs } from "pinia";

import { updateSettings } from "@/api/account";
import { useAccount } from "@/composables/account";
import { usePlayerControls } from "@/composables/player";
import { useNewsStore } from "@/stores/news";

const NEWS_PROVIDERS = [
  {
    key: "srf",
    title: "SRF News",
    language: "DE",
    description: "Jede Stunde 5 Minuten",
    url: "srf.ch/news",
    enabled: true,
  },
  {
    key: "rfi",
    title: "Radio France Info",
    language: "FR",
    description: "Jede Stunde 10 Minuten\n15:00 & 20:00 30 Minuten",
    url: "francetvinfo.fr",
    enabled: true,
  },
  {
    key: "dlf",
    title: "DLF",
    language: "DE",
    description: "-",
    url: "deutschlandfunk.de",
    enabled: false,
  },
  {
    key: "bbc",
    title: "BBC",
    language: "EN",
    description: "-",
    url: "bbc.co.uk/news",
    enabled: false,
  },
];

export const useNews = () => {
  const { settings: userSettings } = useAccount();
  const { playNews, endPlayNews } = usePlayerControls();
  const { schedule, providerKey: localProviderKey } = storeToRefs(useNewsStore());

  // use user settings in case of authenticated, else local storage
  const providerKey: WritableComputedRef<string | null> = computed<string | null>({
    get: () => {
      return userSettings.value ? userSettings.value.newsProvider : localProviderKey.value;
    },
    set: async (value: string | null) => {
      if (userSettings.value) {
        userSettings.value.newsProvider = value ?? "";

        try {
          await updateSettings(userSettings.value);
        } catch (e) {
          console.error(e);
        }
      } else {
        localProviderKey.value = value ?? "";
      }
    },
  });

  const providers = computed(() => {
    return NEWS_PROVIDERS.map((provider) => {
      return {
        ...provider,
        selected: provider.key === providerKey.value,
      };
    });
  });

  const selectedProvider = computed(() => {
    return providers.value.find((provider) => provider.selected) ?? null;
  });

  const setProvider = (key: string | null) => {
    providerKey.value = key;
  };

  return {
    providers,
    providerKey,
    localProviderKey,
    selectedProvider,
    schedule,
    // exposed actions
    setProvider,
    playNews,
    endPlayNews,
  };
};
