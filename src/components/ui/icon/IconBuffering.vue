<script lang="ts">
import { defineComponent, computed } from "vue";
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
        strokeWidth: 3,
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
    <line x1="15" y1="18" x2="15" y2="30" />
    <line x1="21" y1="18" x2="21" y2="30" />
    <line x1="27" y1="18" x2="27" y2="30" />
    <line x1="33" y1="18" x2="33" y2="30" />
  </svg>
</template>
