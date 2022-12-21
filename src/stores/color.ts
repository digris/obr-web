import { ref } from "vue";
import { defineStore } from "pinia";

export const useColorStore = defineStore("color", () => {
  const colors = ref<Map<string, Array<number>>>(new Map());
  const colorByKey = (key: string): Array<number> | undefined => colors.value.get(key);
  // used to populate colors loaded in batch in listings
  // all primary resource types are annotated with `userRating` when requesting via API
  const injectColors = async (list: Array<any>) => {
    list.forEach((item) => {
      const { ct, uid, color } = item;
      if (ct && uid) {
        const key = `${ct}:${uid}`;
        colors.value.set(key, color);
      }
    });
  };
  return {
    colorByKey,
    injectColors,
  };
});
