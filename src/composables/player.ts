import { computed } from "vue";
import { useStore } from "vuex";

const usePlayerState = () => {
  const store = useStore();
  const playerState = computed(() => store.getters["player/playerState"]);
  const isLive = computed(() => playerState.value?.isLive);
  const isOndemand = computed(() => !playerState.value?.isLive);
  const isPlaying = computed(() => playerState.value?.isPlaying);
  const isBuffering = computed(() => playerState.value?.isBuffering);
  const isPaused = computed(() => playerState.value?.isPaused);
  const duration = computed(() => playerState.value?.duration);
  const currentTime = computed(() => playerState.value?.currentTime);
  const relPosition = computed(() => playerState.value?.relPosition);

  const currentMedia = computed(() => store.getters["player/media"]);
  const currentScope = computed(() => store.getters["player/scope"]);
  const currentColor = computed(() => store.getters["player/color"]);

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

    currentMedia,
    currentScope,
    currentColor,
  };
};

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
