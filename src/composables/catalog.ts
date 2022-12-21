import { storeToRefs } from "pinia";

import { useCatalogStore } from "@/stores/catalog";

export const useCatalog = () => {
  const { moods } = storeToRefs(useCatalogStore());
  const { loadMoods } = useCatalogStore();
  return {
    moods,
    loadMoods,
  };
};
