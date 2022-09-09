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
    rotate: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      return {
        stroke: color.value,
        fill: "none",
        strokeWidth: (6.5 * 120) / size.value,
        width: `${size.value}px`,
        height: `${size.value}px`,
        transform: `rotate(${props.rotate}deg)`,
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
    height="120px"
    width="120px"
    viewBox="0 0 120 120"
    :style="style"
  >
    <polyline points="56,100 96,60 56,20" />
    <polyline points="35,100 75,60 35,20" />
  </svg>
</template>
