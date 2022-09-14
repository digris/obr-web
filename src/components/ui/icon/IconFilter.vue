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
        fill: "transparent",
        stroke: color.value,
        strokeWidth: 2.5,
        transform: `rotate(${props.rotate}deg)`,
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
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" :style="style">
    <line x1="16.5" y1="24" x2="12" y2="24" />
    <line x1="36" y1="24" x2="21.5" y2="24" />
    <line x1="26.5" y1="16" x2="12" y2="16" />
    <line x1="36" y1="16" x2="31.5" y2="16" />
    <line x1="21.7" y1="32" x2="12" y2="32" />
    <line x1="36" y1="32" x2="26.5" y2="32" />
    <circle cx="29" cy="16" r="2.5" />
    <circle cx="24" cy="32" r="2.5" />
    <path d="M21.5,24c0,1.4-1.1,2.5-2.5,2.5s-2.5-1.1-2.5-2.5s1.1-2.5,2.5-2.5S21.5,22.6,21.5,24" />
  </svg>
</template>
