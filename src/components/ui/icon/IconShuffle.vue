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
        fill: "none",
        stroke: props.color,
        strokeWidth: (2 * BASE_SIZE) / props.size,
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
    <path d="M26.1,21.9l1.4-1.4c1-1,2.2-1.5,3.5-1.5h5" />
    <path d="M36,29h-5c-1.3,0-2.5-0.5-3.5-1.5l-7-7c-1-1-2.2-1.5-3.5-1.5h-5" />
    <path d="M21.9,26.1l-1.4,1.4c-1,1-2.2,1.5-3.5,1.5h-5" />
    <polygon points="33.2,23.3 33.2,14.8 37.4,19 " />
    <polygon points="33.2,33.2 33.2,24.7 37.4,29 " />
  </svg>
</template>
