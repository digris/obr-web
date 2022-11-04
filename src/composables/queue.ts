import log from "loglevel";
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { shuffle } from "lodash-es";

import type { Media } from "@/typings/api";
import type { AnnotatedMedia } from "@/stores/queue";
import { useDevice } from "@/composables/device";
import { useQueueStore } from "@/stores/queue";
import { useSettingsStore } from "@/stores/settings";
import { getMedia } from "@/api/catalog";
import { usePlayerControls, usePlayerState } from "@/composables/player";

const annotateMedia = (media: Array<Media>, scope: Array<string> = []): Array<AnnotatedMedia> => {
  return media.map((mediaObj: Media) => {
    // @ts-ignore
    const artistKeys = mediaObj.artists.map((artistObj) => {
      return `${artistObj.ct}:${artistObj.uid}`;
    });
    const mappedScope = scope ? [...scope, ...artistKeys] : artistKeys;
    return { ...mediaObj, scope: mappedScope };
  });
};

const useQueueState = () => {
  const {
    previousIndex,
    currentIndex,
    nextIndex,
    currentMedia,
    numMedia,
    media: queuedMedia,
  } = storeToRefs(useQueueStore());

  return {
    previousIndex,
    currentIndex,
    nextIndex,
    currentMedia,
    queueLength: numMedia,
    queuedMedia,
  };
};

const useQueueControls = () => {
  const appBridge = window.appBridge;
  const { isWeb } = useDevice();
  const { playMedia, playLive } = usePlayerControls();
  const { isLive, isPlaying } = usePlayerState();
  const { previousIndex, nextIndex, currentMedia } = storeToRefs(useQueueStore());
  const { shuffleMode } = storeToRefs(useSettingsStore());
  const { enqueue, setIndex, removeAtIndex, clearQueue, shuffleQueue } = useQueueStore();
  const hasPrevious = computed(() => previousIndex.value !== null);
  const hasNext = computed(() => !!isLive);
  const enqueueObj = async (obj: any, mode = "append") => {
    log.debug("queueControls - enqueueObj", obj, mode);
    const objKey = `${obj.ct}:${obj.uid}`;
    const filter = {
      obj_key: objKey,
    };
    const { results } = await getMedia(100, 0, filter);
    console.debug("results", results);
    const scope = [objKey];
    if (isWeb) {
      await enqueue({media: annotateMedia(results, scope), mode});
    } else {
      const channel = "queue:replace";
      const data = annotateMedia(results, scope);
      log.debug("queueControls - enqueueObj app-mode", channel, data);
      await appBridge.send(channel, data);
    }
  };
  const enqueueMedia = async (media: Array<Media>, mode = "append", scope = []) => {
    log.debug("queueControls - enqueueMedia", media, mode, scope);
    if (shuffleMode.value) {
      media = shuffle(media);
    }
    if (isWeb) {
      await enqueue({media: annotateMedia(media, scope), mode});
    } else {
      const channel = "queue:replace";
      const data = annotateMedia(media, scope);
      log.debug("queueControls - enqueueMedia app-mode", channel, data);
      await appBridge.send(channel, data);
    }
  };
  const startPlayCurrent = async (force = false) => {
    if (!isWeb) {
      log.debug("queueControls - startPlayCurrent: ignored in app-mode");
      return;
    }
    if (isPlaying.value && !force) {
      return;
    }
    if (!currentMedia.value) {
      log.warn("unable to play: no current media");
      return;
    }
    try {
      await playMedia(currentMedia.value);
    } catch (e) {
      log.warn("player error - try with next");
      await playNext();
    }
  };
  const playPrevious = async () => {
    log.debug("queueControls - playPrevious");
    if (previousIndex.value !== null) {
      await setIndex(previousIndex.value);
      await startPlayCurrent(true);
    } else {
      throw new Error("no previous media");
    }
  };
  const playNext = async () => {
    log.debug("queueControls - playNext");
    if (nextIndex.value !== null) {
      await setIndex(nextIndex.value);
      await startPlayCurrent(true);
    } else {
      log.info("no next media - switch to live");
      await playLive();
    }
  };
  const playFromIndex = async (index: number) => {
    log.debug("queueControls - playFromIndex", index);
    await setIndex(index);
    await startPlayCurrent(true);
  };
  return {
    // mapped state
    hasPrevious,
    hasNext,
    // mapped actions
    playPrevious,
    playNext,
    playFromIndex,
    removeAtIndex,
    enqueueMedia,
    enqueueObj,
    startPlayCurrent,
    shuffleQueue,
    clearQueue,
  };
};

export { useQueueState, useQueueControls };
