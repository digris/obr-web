<script lang="ts">
import { defineComponent, computed } from "vue";

const BASE_SIZE = 64;

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
        fill: props.color,
        stroke: "transparent",
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
    <path d="M14 30V18H22L32 8V40L22 30ZM17 27H23.35L29 32.45V15.6L23.35 21H17ZM23 24Z" />
  </svg>
</template>
