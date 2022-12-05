import { computed } from "vue";
import log from "loglevel";
import { storeToRefs } from "pinia";
import { shuffle } from "lodash-es";

import { getMedia } from "@/api/catalog";
import { useDevice } from "@/composables/device";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import type { AnnotatedMedia } from "@/stores/queue";
import { useQueueStore } from "@/stores/queue";
import { useSettingsStore } from "@/stores/settings";
import type { Media } from "@/typings/api";

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

const getAppBridgeQueueChannel = (mode: string) => {
  switch (mode) {
    case "insert": {
      return "queue:enqueueAsNext";
    }
    case "append": {
      return "queue:enqueueToEnd";
    }
    default: {
      return "queue:enqueue";
    }
  }
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
  const {
    enqueue,
    setIndex,
    deleteAtIndex: deleteAtIndexWeb,
    clearQueue: clearQueueWeb,
    shuffleQueue: shuffleQueueWeb,
  } = useQueueStore();
  const hasPrevious = computed(() => previousIndex.value !== null);
  const hasNext = computed(() => !!isLive);
  const enqueueObj = async (obj: any, mode = "append") => {
    log.debug("queueControls - enqueueObj", obj, mode);
    const objKey = `${obj.ct}:${obj.uid}`;
    const filter = {
      obj_key: objKey,
    };
    const { results } = await getMedia(100, 0, filter);
    log.debug("results", results);
    const scope = [objKey];
    if (isWeb) {
      await enqueue({ media: annotateMedia(results, scope), mode });
    } else {
      const channel = getAppBridgeQueueChannel(mode);
      const data = annotateMedia(results, scope);
      log.debug("queueControls - enqueueObj app-mode", channel, data);
      await appBridge.send(channel, data);
    }
  };
  const enqueueMedia = async (media: Array<Media>, mode = "append", scope = []) => {
    log.debug("queueControls - enqueueMedia", media, mode, scope);
    if (isWeb) {
      if (shuffleMode.value) {
        media = shuffle(media);
      }
      await enqueue({ media: annotateMedia(media, scope), mode });
    } else {
      const channel = getAppBridgeQueueChannel(mode);
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
    // await playMedia(currentMedia.value);
    try {
      await playMedia(currentMedia.value);
    } catch (e) {
      log.warn("player error - try with next", e);
      await playNext();
    }
  };
  const playFromIndex = async (index: number) => {
    log.debug("queueControls - playFromIndex", index);
    if (isWeb) {
      await setIndex(index);
      await startPlayCurrent(true);
    } else {
      const channel = "queue:playFromIndex";
      const data = {
        index,
      };
      log.debug("queueControls - enqueueMedia app-mode", channel, data);
      await appBridge.send(channel, data);
    }
  };
  const playPrevious = async () => {
    log.debug("queueControls - playPrevious");
    if (previousIndex.value !== null) {
      await playFromIndex(previousIndex.value);
    } else {
      throw new Error("no previous media");
    }
  };
  const playNext = async () => {
    log.debug("queueControls - playNext");
    if (nextIndex.value !== null) {
      log.debug("queueControls - playNext index", nextIndex.value);
      await playFromIndex(nextIndex.value);
    } else {
      log.info("no next media - switch to live");
      await playLive();
    }
  };
  // mapping actions depending on mode
  const clearQueue = async (): Promise<void> => {
    if (isWeb) {
      await clearQueueWeb();
    } else {
      const channel = "queue:clear";
      await appBridge.send(channel);
    }
  };
  const shuffleQueue = async (): Promise<void> => {
    if (isWeb) {
      await shuffleQueueWeb();
    } else {
      const channel = "queue:shuffle";
      await appBridge.send(channel);
    }
  };
  const deleteAtIndex = async (index: number): Promise<void> => {
    if (isWeb) {
      await deleteAtIndexWeb(index);
    } else {
      const channel = "queue:deleteAtIndex";
      const data = {
        index,
      };
      await appBridge.send(channel, data);
    }
  };
  return {
    // mapped state
    hasPrevious,
    hasNext,
    // mapped actions
    playPrevious,
    playNext,
    playFromIndex,
    deleteAtIndex,
    enqueueMedia,
    enqueueObj,
    startPlayCurrent,
    shuffleQueue,
    clearQueue,
  };
};

export { useQueueControls, useQueueState };
