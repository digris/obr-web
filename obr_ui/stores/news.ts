import { ref } from "vue";
import { useStorage } from "@vueuse/core";
import { defineStore } from "pinia";

interface NewsItem {
  provider: string;
  name: string;
  url: string;
}

export const useNewsStore = defineStore("news", () => {
  const schedule = ref<NewsItem[]>([]);
  const providerKey = useStorage("news/provider", "", localStorage, {
    serializer: {
      read: (v) => v,
      write: (v) => v,
    },
  });
  return {
    schedule,
    providerKey,
  };
});
