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
        fill: "none",
        stroke: color.value,
        strokeWidth: 2.75,
        transform: `rotate(${props.rotate}deg)`,
        strokeMiterlimit: 10,
        width: `${size.value}px`,
        height: `${size.value}px`,
      };
    });
    return {
      style,
      color,
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
    <rect x="30" y="16" width="2.5" height="16" stroke="none" :fill="color" />
    <polygon points="26.7,24 15,29.8 15,18.2 "/>
  </svg>
</template>
