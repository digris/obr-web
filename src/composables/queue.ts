import { computed } from "vue";
import { useStore } from "vuex";
import { storeToRefs } from "pinia";
import { shuffle } from "lodash-es";

import { useSettingsStore } from "@/stores/settings";
import { getMedia } from "@/api/catalog";
import { usePlayerState } from "@/composables/player";

const useQueueState = () => {
  const store = useStore();
  const previousIndex = computed(() => store.getters["queue/previousIndex"]);
  const currentIndex = computed(() => store.getters["queue/currentIndex"]);
  const nextIndex = computed(() => store.getters["queue/nextIndex"]);
  const numMedia = computed(() => store.getters["queue/numMedia"]);
  return {
    previousIndex,
    currentIndex,
    nextIndex,
    queueLength: numMedia,
  };
};

const useQueueControls = () => {
  const queue = window.queue;
  const store = useStore();
  const { isLive, isPlaying } = usePlayerState();
  const { previousIndex } = useQueueState();
  const { shuffleMode } = storeToRefs(useSettingsStore());
  const hasPrevious = computed(() => previousIndex.value !== null);
  const hasNext = computed(() => !!isLive);
  const playPrevious = async () => {
    // TODO: handle case of skipping back from live-mode
    await queue.playPrevious();
  };
  const playNext = async () => {
    await queue.playNext();
  };
  const playFromIndex = async (index: number) => {
    await queue.playFromIndex(index);
  };
  const removeAtIndex = async (index: number) => {
    await queue.removeAtIndex(index);
  };
  const enqueueMedia = async (media: Array<object>, mode = "append", scope = []) => {
    if (shuffleMode.value) {
      media = shuffle(media);
    }
    await store.dispatch("queue/enqueue", { media, mode, scope });
    // await queue.startPlayCurrent();
  };
  const enqueueObj = async (obj: object, mode = "append") => {
    // @ts-ignore
    const objKey = `${obj.ct}:${obj.uid}`;
    const filter = {
      obj_key: objKey,
    };
    const { results } = await getMedia(100, 0, filter);
    const scope = [objKey];
    await store.dispatch("queue/enqueue", { media: results, mode, scope });
  };
  const startPlayCurrent = async (force = false) => {
    if (isPlaying.value && !force) {
      return;
    }
    await queue.startPlayCurrent();
  };
  const shuffleQueue = async () => {
    await store.dispatch("queue/shuffleQueue");
  };
  return {
    hasPrevious,
    hasNext,
    playPrevious,
    playNext,
    playFromIndex,
    removeAtIndex,
    enqueueMedia,
    enqueueObj,
    startPlayCurrent,
    shuffleQueue,
  };
};

export { useQueueState, useQueueControls };
