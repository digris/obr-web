import { usePlayerState } from "@/composables/player";
import { useRatingStore } from "@/stores/rating";
import { useScheduleStore } from "@/stores/schedule";

const useRating = () => {
  const { ratingByKey, loadRating, setRating } = useRatingStore();
  const { currentMedia: scheduleMedia } = useScheduleStore();
  const { isLive: playerIsLive, isPlaying: playerIsPlaying, media: playerMedia } = usePlayerState();

  const getRatingSource = (key: string) => {
    // check if the rated item (media in our case) is currently active in the player
    if (playerMedia.value && `${playerMedia.value.ct}:${playerMedia.value.uid}` === key) {
      return playerIsLive.value ? "live" : "ondemand";
    }
    // if player is not playing (eventually user is listening via other source)
    // we check if the item (media in our case) is currently scheduled
    if (!playerIsPlaying.value) {
      if (scheduleMedia && `${scheduleMedia.ct}:${scheduleMedia.uid}` === key) {
        return "live";
      }
    }
    return "ondemand";
  };

  const setRatingWithSource = async (
    key: string,
    value: number | null,
    opts = {}
  ): Promise<number | null> => {
    return await setRating(key, value, {
      ...opts,
      source: getRatingSource(key),
    });
  };

  return {
    ratingByKey,
    loadRating,
    setRating,
    setRatingWithSource,
  };
};

export { useRating };
