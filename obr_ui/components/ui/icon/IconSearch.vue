<script lang="ts" setup>
import { computed } from "vue";

import { useIconSize } from "@/composables/icon";

const props = withDefaults(
  defineProps<{
    scale?: number;
    colorVar?: string;
  }>(),
  {
    scale: 1,
    colorVar: "--c-fg",
  }
);

const { iconSize: size, iconStrokeWidth: strokeWidth } = useIconSize(props.scale);
const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 48 48"
    :style="{
      fill: 'none',
      stroke: color,
      strokeWidth,
      width: `${size}px`,
      height: `${size}px`,
    }"
  >
    <circle cx="23.5" cy="22.8" r="9" />
    <line x1="29.1" y1="28.7" x2="36.5" y2="36.2" />
  </svg>
</template>
