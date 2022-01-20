import { computed } from 'vue';
import { useStore } from 'vuex';
import queue from '@/player/queue';

import { usePlayerState } from '@/composables/player';

const useQueueState = () => {
  const store = useStore();
  const previousIndex = computed(() => store.getters['queue/previousIndex']);
  const currentIndex = computed(() => store.getters['queue/currentIndex']);
  const nextIndex = computed(() => store.getters['queue/nextIndex']);
  const numMedia = computed(() => store.getters['queue/numMedia']);
  return {
    previousIndex,
    currentIndex,
    nextIndex,
    queueLength: numMedia,
  };
};

const useQueueControls = () => {
  const { isLive } = usePlayerState();
  const { previousIndex } = useQueueState();
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
  return {
    hasPrevious,
    hasNext,
    playPrevious,
    playNext,
    playFromIndex,
    removeAtIndex,
  };
};

export {
  useQueueState,
  useQueueControls,
};
