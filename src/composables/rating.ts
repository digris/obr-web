import { computed } from 'vue';
import { useStore } from 'vuex';

const useObjRating = (objKey: string) => {
  const store = useStore();
  const userRating = computed(() => {
    return store.getters['rating/ratingByKey'](objKey);
  });
  const rate = async (value: number) => {
    const vote = {
      key: objKey,
      value,
    };
    await store.dispatch('rating/updateRating', vote);
  };
  const isFavorite = computed(() => {
    return userRating?.value?.value === 1;
  });
  const isBanned = computed(() => {
    return userRating?.value?.value === -1;
  });
  return {
    userRating,
    isFavorite,
    isBanned,
    rate,
  };
};

export {
  useObjRating,
};
