<script lang="ts">
import { defineComponent, ref } from 'vue';

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';

const SIZE = 120;
const ICON_SIZE = 96;

export default defineComponent({
  components: {
    CircleButton,
    IconPlay,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'play',
  ],
  setup(props, { emit }) {
    const size = ref(SIZE);
    const iconSize = ref(ICON_SIZE);
    const play = () => {
      emit('play');
    };
    return {
      size,
      iconSize,
      play,
    };
  },
});
</script>

<template>
  <CircleButton
    :size="size"
    :disabled="disabled"
    :outline-opacity="(1)"
    :outline-width="(6)"
    :outline-on-hover="(true)"
    @click="play"
  >
    <IconPlay
      :size="iconSize"
      color="rgb(var(--c-page-fg))"
    />
  </CircleButton>
</template>
