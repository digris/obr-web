<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';

import CircleProgressButton from '@/components/ui/button/CircleProgressButton.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';
import IconBuffering from '@/components/ui/icon/IconBuffering.vue';
// import IconPause from '@/components/ui/icon/IconPause.vue';
import IconPlaying from '@/components/ui/icon/IconPlaying.vue';

const SIZE = 120;
const ICON_SIZE = 96;

export default defineComponent({
  components: {
    CircleProgressButton,
    IconPlay,
  },
  props: {
    media: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'play',
    'pause',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const isHover = ref(false);
    const size = ref(SIZE);
    const iconSize = ref(ICON_SIZE);
    const playerState = computed(() => store.getters['player/playerState']);
    const currentMedia = computed(() => store.getters['player/media']);
    const isCurrent = computed(() => currentMedia.value?.uid === props.media?.uid);
    const isPlaying = computed(() => {
      if (!isCurrent.value) {
        return false;
      }
      return playerState.value.isPlaying;
    });
    const isBuffering = computed(() => {
      if (!isCurrent.value) {
        return false;
      }
      return playerState.value.isBuffering;
    });
    const progress = computed(() => {
      if (!isCurrent.value) {
        return null;
      }
      return playerState.value && playerState.value.relPosition;
    });
    const icon = computed(() => {
      if (isBuffering.value) {
        return IconBuffering;
      }
      if (isPlaying.value && isHover.value) {
        // return IconPause;
        return IconPlaying;
      }
      if (isPlaying.value) {
        return IconPlaying;
      }
      return IconPlay;
    });
    const isFilled = computed(() => {
      return (isPlaying.value || isBuffering.value);
    });
    const handleClick = () => {
      if (isBuffering.value || isPlaying.value) {
        emit('pause');
      } else {
        emit('play');
      }
    };
    return {
      isHover,
      size,
      iconSize,
      handleClick,
      isCurrent,
      currentMedia,
      isPlaying,
      isBuffering,
      isFilled,
      progress,
      icon,
    };
  },
});
</script>

<template>
  <CircleProgressButton
    @mouseover="isHover = true"
    @mouseleave="isHover = false"
    :size="size"
    :outline-width="(6)"
    :filled="isFilled"
    :progress="progress"
    @click="handleClick"
  >
    <component
      :is="icon"
      :size="iconSize"
      :color="(isFilled) ? 'rgb(var(--c-page-fg-inverse))' : 'rgb(var(--c-page-fg))'"
      :pause="(isPlaying && isHover)"
    />
  </CircleProgressButton>
</template>
