import log from "loglevel";
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useDevice } from "@/composables/device";
import { usePlayerStore } from "@/stores/player";
import { useScheduleStore } from "@/stores/schedule";
import { useQueueStore } from "@/stores/queue";
import { getMediaUrl } from "@/player/media";
import { getStreamUrl } from "@/player/stream";
import type { AnnotatedMedia } from "@/stores/queue";

const usePlayerState = () => {
  const { playerState } = storeToRefs(usePlayerStore());
  const isLive = computed(() => playerState.value?.isLive);
  const isOndemand = computed(() => !playerState.value?.isLive);
  const isPlaying = computed(() => playerState.value?.isPlaying);
  const isBuffering = computed(() => playerState.value?.isBuffering);
  const isPaused = computed(() => playerState.value?.isPaused);
  const duration = computed(() => playerState.value?.duration);
  const currentTime = computed(() => playerState.value?.currentTime);
  const relPosition = computed(() => playerState.value?.relPosition);
  const { currentMedia: scheduleMedia } = storeToRefs(useScheduleStore());
  const { currentMedia: queueMedia } = storeToRefs(useQueueStore());
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

const usePlayerControls = () => {
  const audioPlayer = window.audioPlayer;
  const appBridge = window.appBridge;
  const { isWeb } = useDevice();
  const playMedia = async (media: AnnotatedMedia) => {
    log.debug("playerControls - playMedia", media);
    const url = getMediaUrl(media);
    const { cueIn: startTime, cueOut, fadeIn, fadeOut } = media;
    const endTime = media.duration - cueOut;
    // log.debug("player:playMedia", {
    //   startTime,
    //   endTime,
    //   fadeIn,
    //   fadeOut,
    //   url,
    //   title: `${media.name} - ${media.artistDisplay}`,
    // });
    try {
      await audioPlayer.play(url, startTime, endTime, fadeIn, fadeOut);
    } catch (e) {
      throw Error(`unable to play media: ${e}`);
    }
  };
  const playLive = async (startTime = 0) => {
    if (isWeb) {
      const url = getStreamUrl();
      log.debug("playerControls - playLive web-mode", url);
      await audioPlayer.play(url, startTime);
    } else {
      log.debug("playerControls - playLive app-mode");
      await appBridge.send("player:playLive");
    }
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
    playMedia,
    playLive,
    pause,
    resume,
    seek,
  };
};

export { usePlayerState, usePlayerControls };
