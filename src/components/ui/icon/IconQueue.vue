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
    const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
    const style = computed(() => {
      return {
        stroke: "none",
        fill: color.value,
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
  <!-- eslint-disable max-len -->
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" :style="style">
    <rect x="16" y="14.5" width="20" height="3" />
    <rect x="16" y="22.5" width="20" height="3" />
    <rect x="16" y="30.5" width="20" height="3" />

    <circle cx="12" cy="24" r="2" />
    <circle cx="12" cy="16" r="2" />
    <circle cx="12" cy="32" r="2" />
  </svg>
  <!-- eslint-enable max-len -->
</template>
