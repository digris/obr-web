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
        fill: "transparent",
        stroke: color.value,
        strokeWidth: 3,
        strokeMiterlimit: 10,
        width: `${size.value}px`,
        height: `${size.value}px`,
      };
    });
    return {
      color,
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
    <polygon :stroke="color" points="34.7,24 22,30.4 22,17.6" />
    <polygon
      :fill="color"
      stroke-width="0"
      points="18.2,30.8 18.2,17.2 18.2,14.4 15.8,13.1 15.8,34.9 18.2,33.6"
    />
  </svg>
</template>
