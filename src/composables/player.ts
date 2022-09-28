import { computed } from "vue";
import { useStore } from "vuex";
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/player";
import { useScheduleStore } from "@/stores/schedule";

const usePlayerState = () => {
  const store = useStore();


  const { playerState } = storeToRefs(usePlayerStore());

  // const playerState = computed(() => store.getters["player/playerState"]);
  // const playState = computed(() => store.getters["player/playState"]);
  const isLive = computed(() => playerState.value?.isLive);
  const isOndemand = computed(() => !playerState.value?.isLive);
  const isPlaying = computed(() => playerState.value?.isPlaying);
  const isBuffering = computed(() => playerState.value?.isBuffering);
  const isPaused = computed(() => playerState.value?.isPaused);
  const duration = computed(() => playerState.value?.duration);
  const currentTime = computed(() => playerState.value?.currentTime);
  const relPosition = computed(() => playerState.value?.relPosition);

  // const currentMedia = computed(() => store.getters["player/media"]);
  // const currentScope = computed(() => store.getters["player/scope"]);
  // const currentColor = computed(() => store.getters["player/color"]);

  // moving parts to pinia
  // depending on mode (live / on-demand) we have different sources for "media"
  const { currentMedia: scheduleMedia } = storeToRefs(useScheduleStore());
  const queueMedia = computed(() => store.getters["queue/currentMedia"]);
  const media = computed(() => {
    return isLive.value ? scheduleMedia.value : queueMedia.value;
  });
  const scope = computed(() => {
    return [...(media.value?.scope ?? []), `${media.value?.ct}:${media.value?.uid}`];
  });
  const release = computed(() => {
    return media.value?.releases?.length ? media.value.releases[0] : null;
  });
  const color = computed(() => {
    return release.value?.image?.rgb ?? [0, 0, 0];
  });

  return {
    playerState,
    isLive,
    isOndemand,
    isPlaying,
    isBuffering,
    isPaused,
    duration,
    currentTime,
    relPosition,

    media,
    scope,
    // release,
    color,
  };
};

// const usePlayerState = () => {
//   const store = useStore();
//   const playerState = computed(() => store.getters["player/playerState"]);
//   const isLive = computed(() => playerState.value?.isLive);
//   const isOndemand = computed(() => !playerState.value?.isLive);
//   const isPlaying = computed(() => playerState.value?.isPlaying);
//   const isBuffering = computed(() => playerState.value?.isBuffering);
//   const isPaused = computed(() => playerState.value?.isPaused);
//   const duration = computed(() => playerState.value?.duration);
//   const currentTime = computed(() => playerState.value?.currentTime);
//   const relPosition = computed(() => playerState.value?.relPosition);
//
//   const currentMedia = computed(() => store.getters["player/media"]);
//   const currentScope = computed(() => store.getters["player/scope"]);
//   const currentColor = computed(() => store.getters["player/color"]);
//
//   return {
//     playerState,
//     isLive,
//     isOndemand,
//     isPlaying,
//     isBuffering,
//     isPaused,
//     duration,
//     currentTime,
//     relPosition,
//
//     currentMedia,
//     currentScope,
//     currentColor,
//   };
// };

const usePlayerControls = () => {
  const audioPlayer = window.audioPlayer;
  const play = (url: string, startTime = 0) => {
    audioPlayer.play(url, startTime);
  };
  const pause = () => {
    audioPlayer.pause();
  };
  const resume = () => {
    audioPlayer.resume();
  };
  const seek = (pos: number) => {
    audioPlayer.seek(pos);
  };
  return {
    play,
    pause,
    resume,
    seek,
  };
};

export { usePlayerState, usePlayerControls };
