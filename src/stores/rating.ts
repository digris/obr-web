import { ref } from "vue";
import { defineStore } from "pinia";
import { getRating, postRating } from "@/api/rating";

export const useRatingStore = defineStore("rating", () => {
  // "state"
  const ratings = ref<Map<string, number | null>>(new Map());
  // "getters"
  const ratingByKey = (key: string): number | null | undefined => ratings.value.get(key);
  // "actions"
  const loadRating = async (key: string): Promise<number | null> => {
    const rating = await getRating(key);
    ratings.value.set(key, rating.value);
    return rating.value;
  };
  // immediately sets the rating for fast ui response, then passes the value to the API
  const setRating = async (
    key: string,
    value: number | null,
    opts = {}
  ): Promise<number | null> => {
    ratings.value.set(key, value);
    const rating = await postRating(key, value, opts);
    ratings.value.set(key, rating.value);
    return rating.value;
  };
  // used to populate ratings loaded in patch in listings
  // all primary resource types are annotated with `userRating` when requesting via API
  const injectRatings = async (list: Array<any>) => {
    list.forEach((item) => {
      const { ct, uid, userRating } = item;
      // console.debug("injectRatings", ct, uid, userRating, item.name);
      if (ct && uid) {
        const key = `${ct}:${uid}`;
        ratings.value.set(key, userRating);
      }
    });
  };
  /*
  const injectRatings = async (newRatings: Array<Map<string, number | null>>) => {
    console.debug("stores/rating - injectRatings", newRatings);
  };
  */
  return {
    ratingByKey,
    loadRating,
    setRating,
    injectRatings,
  };
});
