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
    volume: {
      type: [Number, String],
      default: 1,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
    const style = computed(() => {
      return {
        fill: "none",
        stroke: color.value,
        strokeWidth: (2.5 * 48) / size.value,
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
    <polygon points="19.1,20.1 13.5,20.1 13.5,27.7 19.1,27.7 26.6,34 26.6,13.8" />
    <path
      v-if="volume > 0"
      :stroke-opacity="volume"
      d="M31.9,19.1c1.6,1.3,2.6,3.2,2.6,5.3c0,2-1,3.9-2.6,5.2"
    />
    <line v-if="volume === 0" x1="12" y1="12" x2="36" y2="36" />
  </svg>
</template>
