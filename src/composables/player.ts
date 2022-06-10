import { computed } from "vue";
import { useStore } from "vuex";
import eventBus from "@/eventBus";

const usePlayer = () => {

};

const usePlayerState = () => {
  const store = useStore();
  const playerState = computed(() => store.getters["player/playerState"]);
  const isLive = computed(() => playerState.value?.isLive);
  const isPlaying = computed(() => playerState.value?.isPlaying);
  const isBuffering = computed(() => playerState.value?.isBuffering);
  const issPaused = computed(() => playerState.value?.isPaused);
  const duration = computed(() => playerState.value?.duration);
  const currentTime = computed(() => playerState.value?.currentTime);
  const relPosition = computed(() => playerState.value?.relPosition);

  const currentMedia = computed(() => store.getters["player/media"]);
  const currentScope = computed(() => store.getters["player/scope"]);
  const currentColor = computed(() => store.getters["player/color"]);

  return {
    playerState,
    isLive,
    isPlaying,
    isBuffering,
    issPaused,
    duration,
    currentTime,
    relPosition,

    currentMedia,
    currentScope,
    currentColor,
  };
};

const usePlayerControls = () => {
  const play = () => {
    eventBus.emit("player:controls", { do: "play" });
  };
  const pause = () => {
    eventBus.emit("player:controls", { do: "pause" });
  };
  const resume = () => {
    eventBus.emit("player:controls", { do: "resume" });
  };
  const seek = (pos: number) => {
    const event = {
      do: "seek",
      relPosition: pos,
    };
    eventBus.emit("player:controls", event);
  };
  return {
    play,
    pause,
    resume,
    seek,
  };
};

export { usePlayerState, usePlayerControls };
