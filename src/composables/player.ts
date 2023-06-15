import { computed } from "vue";
import { storeToRefs } from "pinia";

import { useDevice } from "@/composables/device";
import type { CueFade } from "@/player/hlsPlayer";
import { usePlayerStore } from "@/stores/player";
import type { AnnotatedMedia } from "@/stores/queue";
import { useQueueStore } from "@/stores/queue";
import { useScheduleStore } from "@/stores/schedule";

export const usePlayerState = () => {
  const {
    isVisible,
    mode,
    isLive,
    isOndemand,
    isBuffering,
    isPlaying,
    isPaused,
    playState,
    duration,
    currentTime,
    relPosition,
    liveLatency,
    bandwidth,
    //
    debugData,
  } = storeToRefs(usePlayerStore());

  const { currentMedia: scheduleMedia, nextMedia: scheduleNextMedia } = storeToRefs(useScheduleStore());
  const { currentMedia: queueMedia, nextMedia: queueNextMedia } = storeToRefs(useQueueStore());

  const media = computed(() => {
    return isLive.value ? scheduleMedia.value : queueMedia.value;
  });

  const nextMedia = computed(() => {
    if (isLive.value) {
      return scheduleNextMedia.value;
    }
    return queueNextMedia.value ? queueNextMedia.value : scheduleMedia.value;
  });

  const scope = computed(() => {
    if (!media.value) {
      return [];
    }
    // @ts-ignore
    return [...(media.value?.scope ?? []), `${media.value.ct}:${media.value.uid}`];
  });

  const image = computed(() => {
    const release = media.value?.releases?.length ? media.value.releases[0] : null;
    return release ? release.image : null;
  });

  const color = computed(() => {
    return image.value?.rgb ?? [0, 0, 0];
  });

  return {
    isVisible,
    mode,
    isLive,
    isOndemand,
    isBuffering,
    isPlaying,
    isPaused,
    playState,
    duration,
    currentTime,
    relPosition,
    liveLatency,
    bandwidth,
    //
    media,
    nextMedia,
    scope,
    image,
    color,
    //
    debugData,
  };
};

export const usePlayerControls = () => {
  const player = window.hlsPlayer;
  const appBridge = window.appBridge;

  const { setVisibility } = usePlayerStore();

  const { isWeb } = useDevice();

  // web-mode controls
  const playLive = async () => {
    setVisibility(true);
    await player.playLive();
  };
  const playUid = async (uid: string, estimatedDuration?: number, cueFade?: CueFade) => {
    setVisibility(true);
    await player.playUid(uid, estimatedDuration, cueFade);
  };
  const playMedia = async (media: AnnotatedMedia) => {
    const uid = media?.uid ?? "";
    const estimatedDuration = media?.duration ?? 0;
    const cueFade = {
      cueIn: media?.cueIn ?? 0,
      cueOut: media?.cueOut ?? 0,
      fadeIn: media?.fadeIn ?? 0,
      fadeOut: media?.fadeOut ?? 0,
    };
    console.debug("playMedia", uid, cueFade);
    await playUid(uid, estimatedDuration, cueFade);
  };
  const pause = () => player.pause();
  const resume = () => player.resume();
  const seek = (pos: number) => player.seek(pos);

  // app-mode controls
  const appPlayLive = async () => {
    await appBridge.send("player:playLive");
  };
  const appPause = async () => {
    await appBridge.send("player:pause");
  };
  const appResume = async () => {
    await appBridge.send("player:resume");
  };
  const appSeek = async (pos: number) => {
    await appBridge.send("player:seek", { to: pos });
  };

  return {
    playLive: isWeb ? playLive : appPlayLive,
    playMedia,
    pause: isWeb ? pause : appPause,
    resume: isWeb ? resume : appResume,
    seek: isWeb ? seek : appSeek,
  };
};

export const useAnalyser = () => {
  const player = window.hlsPlayer;

  return {
    analyser: player.analyser,
  };
};
