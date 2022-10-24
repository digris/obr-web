import { computed } from "vue";
// import { useStore } from "vuex";
import { storeToRefs } from "pinia";
import { shuffle } from "lodash-es";

import type { Media } from "@/typings/api";
import type { AnnotatedMedia } from "@/stores/queue";
import { useQueueStore } from "@/stores/queue";
import { useSettingsStore } from "@/stores/settings";
import { getMedia } from "@/api/catalog";
import { usePlayerState } from "@/composables/player";
import { getMediaUrl } from "@/player/media";
import { playStream } from "@/player/stream";

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
  const audioPlayer = window.audioPlayer;
  const { isLive, isPlaying } = usePlayerState();
  const { previousIndex, nextIndex, currentMedia } = storeToRefs(useQueueStore());
  const { shuffleMode } = storeToRefs(useSettingsStore());
  const { enqueue, setIndex, removeAtIndex, clearQueue, shuffleQueue } = useQueueStore();
  // const { enqueue } = storeToRefs(useQueueStore());
  const hasPrevious = computed(() => previousIndex.value !== null);
  const hasNext = computed(() => !!isLive);
  const enqueueObj = async (obj: any, mode = "append") => {
    console.debug("queue - enqueueObj", obj, mode);
    const objKey = `${obj.ct}:${obj.uid}`;
    const filter = {
      obj_key: objKey,
    };
    const { results } = await getMedia(100, 0, filter);
    const scope = [objKey];
    console.debug(scope, results);
    await enqueue({ media: annotateMedia(results, scope), mode });
  };
  const enqueueMedia = async (media: Array<Media>, mode = "append", scope = []) => {
    console.debug("queue - enqueueMedia", media, mode, scope);
    if (shuffleMode.value) {
      media = shuffle(media);
    }
    await enqueue({ media: annotateMedia(media, scope), mode });
  };
  const startPlayCurrent = async (force = false) => {
    console.debug("queue - startPlayCurrent", force);
    if (isPlaying.value && !force) {
      return;
    }
    // await queue.startPlayCurrent();
    const media = currentMedia.value;
    console.debug("CM", media);
    if (!media) {
      console.warn("unable to play: no current media");
      return;
    }
    const url = getMediaUrl(media);
    const { cueIn: startTime, cueOut, fadeIn, fadeOut } = media;
    const endTime = media.duration - cueOut;
    console.debug("queue:startPlayCurrent", {
      startTime,
      endTime,
      fadeIn,
      fadeOut,
      url,
      title: `${media.name} - ${media.artistDisplay}`,
    });
    try {
      await audioPlayer.play(url, startTime, endTime, fadeIn, fadeOut);
    } catch (e) {
      console.debug('player error - try with next');
      await playNext();
    }
  };
  const playPrevious = async () => {
    console.debug("queue - playPrevious");
    if (previousIndex.value !== null) {
      await setIndex(previousIndex.value);
      await startPlayCurrent(true);
    } else {
      throw new Error("no previous media");
    }
  };
  const playNext = async () => {
    console.debug("queue - playNext");
    if (nextIndex.value !== null) {
      await setIndex(nextIndex.value);
      await startPlayCurrent(true);
    } else {
      console.info("no next media - switch to live");
      playStream();
    }
  };
  const playFromIndex = async (index: number) => {
    console.debug("queue - playFromIndex", index);
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
