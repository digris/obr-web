<script lang="ts">
import { computed, defineComponent } from "vue";

const BASE_SIZE = 120;

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
        strokeWidth: "6px",
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
    height="120px"
    width="120px"
    viewBox="0 0 120 120"
    :style="style"
  >
    <polyline points="56,100 96,60 56,20" />
    <polyline points="35,100 75,60 35,20" />
  </svg>
</template>
