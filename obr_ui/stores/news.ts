import { ref } from "vue";
import { defineStore } from "pinia";

interface NewsItem {
  provider: string;
  name: string;
  url: string;
}

export const useNewsStore = defineStore("news", () => {
  const schedule = ref<NewsItem[]>([]);
  return {
    schedule,
  };
});
