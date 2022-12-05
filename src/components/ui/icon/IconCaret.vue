<script lang="ts">
import { computed, defineComponent } from "vue";

import { useIconSize } from "@/composables/icon";

enum Rotate {
  down = 0,
  left = 90,
  up = 180,
  right = 270,
}

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
    direction: {
      type: String,
      default: Rotate.right,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      const rotate: Rotate = Rotate[props.direction as keyof typeof Rotate];
      return {
        fill: "none",
        stroke: color.value,
        strokeWidth: (3 * 48) / size.value,
        strokeMiterlimit: 10,
        width: `${size.value}px`,
        height: `${size.value}px`,
        transform: `rotate(${rotate}deg)`,
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
