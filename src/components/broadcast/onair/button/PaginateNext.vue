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
    :outlined="(!disabled)"
  >
    <IconSkip
      :size="iconSize"
      :rotate="rotate"
      color="rgb(var(--c-page-fg))"
    />
  </CircleButton>
</template>
