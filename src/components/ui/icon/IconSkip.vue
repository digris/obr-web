<script lang="ts">
import { computed, defineComponent } from "vue";

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: "rgb(var(--c-page-bg))",
    },
    rotate: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: "transparent",
        stroke: props.color,
        strokeWidth: 2.5,
        transform: `scale(${props.size / BASE_SIZE}) rotate(${props.rotate}deg)`,
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
    <polygon points="30,24 15,15 15,33" />
    <rect x="33.5" y="15" width="0.1" height="18" />
  </svg>
</template>
