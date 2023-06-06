import { storeToRefs } from "pinia";

import { useDevice } from "@/composables/device";
import type { CueFade } from "@/proto/player/hlsPlayer";
import { HlsPlayer } from "@/proto/player/hlsPlayer";
import { useHlsPlayerStore } from "@/proto/stores/player";
import type { AnnotatedMedia } from "@/stores/queue";
// import { useQueueStore } from "@/stores/queue";
// import { useScheduleStore } from "@/stores/schedule";

export const usePlayerState = () => {
  const {
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
    //
    debugData,
  } = storeToRefs(useHlsPlayerStore());

  // const { currentMedia: scheduleMedia, next: scheduleNextMedia } = storeToRefs(useScheduleStore());
  // const { currentMedia: queueMedia, nextMedia: queueNextMedia } = storeToRefs(useQueueStore());
  //
  // const media = computed(() => {
  //   return isLive.value ? scheduleMedia.value : queueMedia.value;
  // });
  //
  // const nextMedia = computed(() => {
  //   if (isLive.value) {
  //     return scheduleNextMedia.value;
  //   }
  //   return queueNextMedia.value ? queueNextMedia.value : scheduleMedia.value;
  // });

  return {
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
    //
    debugData,
  };
};

export const usePlayerControls = () => {
  const player = HlsPlayer.getInstance();
  const appBridge = window.appBridge;

  const { isWeb } = useDevice();

  // web-mode controls
  const playLive = async () => player.playLive();
  const playUid = async (uid: string, estimatedDuration?: number, cueFade?: CueFade) => {
    return await player.playUid(uid, estimatedDuration, cueFade);
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
    console.debug("playMedia", uid, cueFade, media);
    await playUid(uid, estimatedDuration, cueFade);
  };
  const pause = () => player.pause();
  const resume = () => player.resume();
  const seek = (pos: number) => player.seek(pos);

  // app-mode controls
  const appPlayLive = async () => {
    return await appBridge.send("player:playLive");
  };
  const appPause = async () => {
    return await appBridge.send("player:pause");
  };
  const appResume = async () => {
    return await appBridge.send("player:resume");
  };
  const appSeek = async (pos: number) => {
    return await appBridge.send("player:seek", { to: pos });
  };

  return {
    playLive: isWeb ? playLive : appPlayLive,
    playMedia,
    pause: isWeb ? pause : appPause,
    resume: isWeb ? resume : appResume,
    seek: isWeb ? seek : appSeek,
  };
};
