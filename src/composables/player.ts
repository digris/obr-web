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
  const {
    mode,
    state,
    isLive,
    isOndemand,
    isPlaying,
    isBuffering,
    isPaused,
    duration,
    absPosition,
    relPosition,
  } = storeToRefs(usePlayerStore());

  const { currentMedia: scheduleMedia } = storeToRefs(useScheduleStore());
  const { currentMedia: queueMedia } = storeToRefs(useQueueStore());
  const media = computed(() => {
    return isLive.value ? scheduleMedia.value : queueMedia.value;
  });
  const scope = computed(() => {
    // @ts-ignore
    return [...(media.value?.scope ?? []), `${media.value?.ct}:${media.value?.uid}`];
  });
  const release = computed(() => {
    return media.value?.releases?.length ? media.value.releases[0] : null;
  });
  const image = computed(() => {
    // @ts-ignore
    return release.value?.image ?? null;
  });
  const color = computed(() => {
    return image.value?.rgb ?? [0, 0, 0];
  });

  return {
    mode,
    state,
    isLive,
    isOndemand,
    isPlaying,
    isBuffering,
    isPaused,
    duration,
    absPosition,
    relPosition,
    media,
    scope,
    image,
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
  const pause = async () => {
    if (isWeb) {
      // TODO: investigate - when calling from mediaSession audioPlayer is undefined
      window.audioPlayer.pause();
    } else {
      await appBridge.send("player:pause");
    }
  };
  const resume = async () => {
    if (isWeb) {
      // TODO: investigate - when calling from mediaSession audioPlayer is undefined
      window.audioPlayer.resume();
    } else {
      await appBridge.send("player:resume");
    }
  };
  const seek = async (pos: number) => {
    if (isWeb) {
      // TODO: investigate - when calling from mediaSession audioPlayer is undefined
      window.audioPlayer.seek(pos);
    } else {
      await appBridge.send("player:seek", { pos });
    }
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
