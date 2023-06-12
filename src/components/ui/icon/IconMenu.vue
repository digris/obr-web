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
      fill: color,
      stroke: 'none',
      width: `${size}px`,
      height: `${size}px`,
    }"
  >
    <rect x="10" y="13.5" width="28" :height="strokeWidth" />
    <rect x="10" y="22.5" width="28" :height="strokeWidth" />
    <rect x="10" y="31.5" width="28" :height="strokeWidth" />
  </svg>
</template>
