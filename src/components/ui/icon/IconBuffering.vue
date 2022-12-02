<script lang="ts">
import { defineComponent, computed } from "vue";
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
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      return {
        fill: "none",
        stroke: color.value,
        strokeWidth: 3,
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
    <line x1="15" y1="14" x2="15" y2="34" />
    <line x1="21" y1="14" x2="21" y2="34" />
    <line x1="27" y1="14" x2="27" y2="34" />
    <line x1="33" y1="14" x2="33" y2="34" />
  </svg>
</template>

<style lang="scss" scoped>
@keyframes buffering {
  0% {
    transform: scaleY(100%);
  }
  80% {
    transform: scaleY(10%);
  }
  100% {
    transform: scaleY(100%);
  }
}

svg {
  line {
    transform-origin: center;
    animation: buffering 1200ms infinite;
    &:nth-child(1) {
      animation-delay: -600ms;
    }
    &:nth-child(2) {
      animation-delay: -450ms;
    }
    &:nth-child(3) {
      animation-delay: -300ms;
    }
    &:nth-child(4) {
      animation-delay: -150ms;
    }
  }
}
</style>
