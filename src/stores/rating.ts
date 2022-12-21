import { ref } from "vue";
import { defineStore } from "pinia";

import { getRating, postRating } from "@/api/rating";

export const useRatingStore = defineStore("rating", () => {
  const ratings = ref<Map<string, number | null>>(new Map());
  const ratingByKey = (key: string): number | null | undefined => ratings.value.get(key);
  const loadRating = async (key: string): Promise<number | null> => {
    const rating = await getRating(key);
    ratings.value.set(key, rating.value);
    return rating.value;
  };
  const setRating = async (
    key: string,
    value: number | null,
    opts = {}
  ): Promise<number | null> => {
    // immediately sets the rating for fast ui response, then passes the value to the API
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
      console.debug("inject rating", ct, uid, userRating);
      if (ct && uid) {
        const key = `${ct}:${uid}`;
        ratings.value.set(key, userRating);
      }
    });
  };
  return {
    ratingByKey,
    loadRating,
    setRating,
    injectRatings,
  };
});
