import type { Vote } from "@/typings/api";
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { getRating } from "@/api/rating";

export const useRatingStore = defineStore("rating", () => {
  // "state"
  const votes = ref<Array<Vote>>([]);
  // "getters"
  const voteByObjKey = (key: string): Vote | null => {
    console.debug('voteByObjKey', key);
    return votes.value.find((vote) => vote.key === key) || null;
  };
  // "actions"
  const fetchVote = async (key: string) => {
    const rating = await getRating(key);
    console.debug("rating", rating);
  };
  return {
    votes,
    voteByObjKey,
    fetchVote,
  };
});
