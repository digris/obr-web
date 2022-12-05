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
    outlined: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      return {
        fill: color.value,
        stroke: "none",
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
  <!-- eslint-disable max-len -->
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <transition name="fade">
      <path
        v-if="outlined"
        d="M35.3,15.2c-3-3.1-7.8-3.2-10.9-0.1l-0.1,0.1c-0.1,0.1-0.2,0.2-0.2,0.2c-0.1-0.1-0.1-0.2-0.2-0.2c-3-3.1-7.8-3.2-10.9-0.1
        l-0.1,0.1c-1.5,1.5-2.3,3.5-2.3,5.6s0.8,4.1,2.3,5.6L24,37.8l11.3-11.5c1.5-1.5,2.3-3.5,2.3-5.6S36.8,16.6,35.3,15.2z M33.1,24.2
        L24,33.6l-9.1-9.3c-1.9-1.9-1.9-5.1,0-7l0.1-0.1c1-0.9,2.1-1.4,3.3-1.4c1.2,0,2.4,0.5,3.4,1.5c0.4,0.4,0.7,0.9,1,1.4l0.3,0.8h2
        l0.3-0.8c0.2-0.5,0.5-1,1-1.4l0.1-0.1c1.9-1.9,4.9-1.8,6.7,0.1C35.1,19.2,35.1,22.3,33.1,24.2z"
      />
      <path
        v-else
        d="M35.3,15.2c-3-3.1-7.8-3.2-10.9-0.1l-0.1,0.1c-0.1,0.1-0.2,0.2-0.2,0.2c-0.1-0.1-0.1-0.2-0.2-0.2
        c-3-3.1-7.8-3.2-10.9-0.1l-0.1,0.1c-1.5,1.5-2.3,3.5-2.3,5.6s0.8,4.1,2.3,5.6L24,37.8l11.3-11.5c1.5-1.5,2.3-3.5,2.3-5.6
        S36.8,16.6,35.3,15.2z"
      />
    </transition>
  </svg>
  <!-- eslint-enable max-len -->
</template>

<style lang="scss" scoped>
svg {
  path {
    shape-rendering: geometricprecision;
  }
}

.fade-enter-active {
  transition: opacity 200ms;
}

.fade-leave-active {
  transition: opacity 200ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>
