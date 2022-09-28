import type { Vote } from "@/typings/api";
import { defineStore } from "pinia";
import { getRating } from "@/api/rating";

interface State {
  ratings: Array<Vote>;
}

export const useRatingStore = defineStore("rating", {
  state: (): State => ({
    ratings: [],
  }),
  getters: {
    // getVoteByKey(state: State): Vote | null {
    //   return (key: string) => {
    //     return {
    //       key: key,
    //       value: 1,
    //     };
    //   };
    // },
    getRatingByKey:
      (state: State) =>
      (key: string): Vote | null => {
        return state.ratings.find((vote) => vote.key === key) || null;
      },
  },
  actions: {
    async loadRating(key: string): Promise<void> {
      const rating = await getRating(key);
      console.debug("rating", rating);
    },
  },
});
