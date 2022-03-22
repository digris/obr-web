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
  },
  setup(props) {
    const style = computed(() => {
      return {
        stroke: props.color,
        strokeWidth: 3,
        strokeMiterlimit: 10,
        fill: "transparent",
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
    <circle cx="23.5" cy="23" r="7" />
    <line x1="27.5" y1="28" x2="33.5" y2="34" />
  </svg>
</template>
