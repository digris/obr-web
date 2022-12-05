<script lang="ts">
import { computed, defineComponent } from "vue";

import { useIconSize } from "@/composables/icon";

export default defineComponent({
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: "--c-fg",
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      return {
        fill: "none",
        stroke: color.value,
        strokeWidth: (2 * 48) / size.value,
        width: `${size.value}px`,
        height: `${size.value}px`,
      };
    });
    return {
      style,
    };
  },
});
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <path d="M26.1,21.9l1.4-1.4c1-1,2.2-1.5,3.5-1.5h5" />
    <path d="M36,29h-5c-1.3,0-2.5-0.5-3.5-1.5l-7-7c-1-1-2.2-1.5-3.5-1.5h-5" />
    <path d="M21.9,26.1l-1.4,1.4c-1,1-2.2,1.5-3.5,1.5h-5" />
    <polygon points="33.2,23.3 33.2,14.8 37.4,19 " />
    <polygon points="33.2,33.2 33.2,24.7 37.4,29 " />
  </svg>
</template>
