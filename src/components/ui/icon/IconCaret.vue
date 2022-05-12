<script lang="ts">
import { defineComponent, computed } from "vue";

const BASE_SIZE = 48;

enum Rotate {
  down = 0,
  left = 90,
  up = 180,
  right = 270,
}

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
    direction: {
      type: String,
      default: "right",
    },
  },
  setup(props) {
    const style = computed(() => {
      const rotate = Rotate[props.direction];
      return {
        fill: "none",
        stroke: props.color,
        strokeWidth: (2 * BASE_SIZE) / props.size,
        strokeMiterlimit: 10,
        transform: `scale(${props.size / BASE_SIZE}) rotate(${rotate}deg)`,
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
    <polyline points="34,20 24,30 14,20 " />
  </svg>
</template>

<style lang="scss" scoped>
svg {
  &:hover {
    background: transparent;
  }
}
</style>
