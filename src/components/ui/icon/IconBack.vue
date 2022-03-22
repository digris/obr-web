<script lang="ts">
import { defineComponent, computed } from "vue";

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: "rgb(var(--c-page-fg))",
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        stroke: props.color,
        fill: "transparent",
        strokeWidth: (3 * BASE_SIZE) / props.size,
        transform: `scale(${props.size / BASE_SIZE})`,
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
    <line x1="12.5" y1="24" x2="35.5" y2="24" />
    <polyline points="22,33 13,24 22,15 " />
  </svg>
</template>
