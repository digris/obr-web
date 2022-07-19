<script lang="ts">
import { defineComponent, ref } from "vue";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconPaginate from "@/components/ui/icon/IconPaginate.vue";

const SIZE = 120;
const ICON_SIZE = 120;

export default defineComponent({
  components: {
    CircleButton,
    IconPaginate,
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
  <CircleButton :size="size" :disabled="disabled">
    <IconPaginate :size="iconSize" :rotate="rotate" color="rgb(var(--c-page-fg))" />
  </CircleButton>
</template>
