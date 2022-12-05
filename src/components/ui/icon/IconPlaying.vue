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
    <line x1="15" y1="0" x2="15" y2="16" />
    <line x1="21" y1="0" x2="21" y2="16" />
    <line x1="27" y1="0" x2="27" y2="16" />
    <line x1="33" y1="0" x2="33" y2="16" />
  </svg>
</template>

<style lang="scss" scoped>
@keyframes eq {
  0%,
  80%,
  100% {
    transform: scaleY(40%);
  }

  35% {
    transform: scaleY(100%);
  }

  50% {
    transform: scaleY(60%);
  }

  /* stylelint-disable-next-line keyframe-block-no-duplicate-selectors */
  80% {
    transform: scaleY(80%);
  }
}

svg {
  transform: rotate(180deg) translateY(32%);

  line {
    animation: eq 1200ms infinite;

    &:nth-child(1) {
      animation-delay: -550ms;
    }

    &:nth-child(2) {
      animation-delay: -700ms;
    }

    &:nth-child(3) {
      animation-delay: -350ms;
    }

    &:nth-child(4) {
      animation-delay: -250ms;
    }
  }
}
</style>
