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
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <!-- eslint-disable max-len -->
    <rect x="14" y="8" width="3.2" height="3.2" />
    <rect x="30.8" y="8" width="3.2" height="3.2" />
    <path
      d="M34,11.2v3.2h-3.2v-3.2H17.2v3.2H14v-3.2h-4v25.6h28V11.2H34z M15.6,32c-0.9,0-1.6-0.7-1.6-1.6s0.7-1.6,1.6-1.6
      c0.9,0,1.6,0.7,1.6,1.6S16.5,32,15.6,32z M15.6,27.2c-0.9,0-1.6-0.7-1.6-1.6c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6
      C17.2,26.5,16.5,27.2,15.6,27.2z M15.6,22.4c-0.9,0-1.6-0.7-1.6-1.6c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6
      C17.2,21.7,16.5,22.4,15.6,22.4z M21.2,32c-0.9,0-1.6-0.7-1.6-1.6s0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6S22.1,32,21.2,32z
      M21.2,27.2c-0.9,0-1.6-0.7-1.6-1.6c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6C22.8,26.5,22.1,27.2,21.2,27.2z M21.2,22.4
      c-0.9,0-1.6-0.7-1.6-1.6c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6C22.8,21.7,22.1,22.4,21.2,22.4z M26.8,32
      c-0.9,0-1.6-0.7-1.6-1.6s0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6S27.7,32,26.8,32z M26.8,27.2c-0.9,0-1.6-0.7-1.6-1.6
      c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6C28.4,26.5,27.7,27.2,26.8,27.2z M26.8,22.4c-0.9,0-1.6-0.7-1.6-1.6
      c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6C28.4,21.7,27.7,22.4,26.8,22.4z M32.4,32c-0.9,0-1.6-0.7-1.6-1.6s0.7-1.6,1.6-1.6
      c0.9,0,1.6,0.7,1.6,1.6S33.3,32,32.4,32z M32.4,27.2c-0.9,0-1.6-0.7-1.6-1.6c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6
      C34,26.5,33.3,27.2,32.4,27.2z M32.4,22.4c-0.9,0-1.6-0.7-1.6-1.6c0-0.9,0.7-1.6,1.6-1.6c0.9,0,1.6,0.7,1.6,1.6
      C34,21.7,33.3,22.4,32.4,22.4z"
    />
    <!-- eslint-enable max-len -->
  </svg>
</template>
