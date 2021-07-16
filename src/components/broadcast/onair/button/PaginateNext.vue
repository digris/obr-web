<script lang="ts">
import { defineComponent, ref } from 'vue';

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconSkip from '@/components/ui/icon/IconSkip.vue';

const SIZE = 120;
const ICON_SIZE = 80;

export default defineComponent({
  components: {
    CircleButton,
    IconSkip,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    rotate: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    const size = ref(SIZE);
    const iconSize = ref(ICON_SIZE);
    return {
      size,
      iconSize,
    };
  },
});
</script>

<template>
  <CircleButton
    :size="size"
    :disabled="disabled"
    :outline-opacity="(1)"
    :outline-width="(3)"
  >
    <IconSkip
      :size="iconSize"
      :rotate="rotate"
      color="rgb(var(--c-live-fg))"
    />
  </CircleButton>
</template>
