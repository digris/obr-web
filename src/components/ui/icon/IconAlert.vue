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
        strokeWidth: 2.5,
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
    <path
      d="M31.3,20.3C31.3,27.7,35,35,35,35H13c0,0,3.7-7.2,3.7-14.6c0-4.1,3.3-7.3,7.3-7.3S31.3,16.3,31.3,20.3z"
    />
    <line x1="24" y1="13" x2="24" y2="9.3" />
    <path d="M24,41.5c1.7,0,3-1.3,3-3h-6C21,40.2,22.3,41.5,24,41.5z" />
  </svg>
</template>
