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
        stroke: color.value,
        fill: "none",
        strokeWidth: (2 * 48) / size.value,
        // strokeWidth: 1,
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
    <polyline points="34,19.1 20.2,33 14,34 15.1,27.8 28.9,14 " />
    <path d="M25.3,16.6" />
    <line x1="28.9" y1="14" x2="34" y2="19.1" />
    <line x1="24.8" y1="18.1" x2="29.9" y2="23.2" />
  </svg>
</template>
