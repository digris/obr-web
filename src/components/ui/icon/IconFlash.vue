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
    outlined: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      const baseStyle = {
        fill: "none",
        stroke: color.value,
        strokeMiterlimit: 10,
        strokeWidth: (2.5 * 48) / size.value,
        width: `${size.value}px`,
        height: `${size.value}px`,
      };
      if (props.outlined) {
        return baseStyle;
      }
      return {
        ...baseStyle,
        fill: color.value,
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
    <polygon points="35,21 24,21 24,13 13,26 24,26 24,35" />
  </svg>
  <!-- eslint-enable max-len -->
</template>

<style lang="scss" scoped>
svg {
  path {
    shape-rendering: geometricprecision;
  }
}
</style>
