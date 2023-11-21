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
    flipY: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
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
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 48 48"
    :style="style"
    :class="{
      'flip-y': flipY,
    }"
  >
    <rect x="14" y="26" width="20" height="3" />
    <rect x="14" y="32" width="20" height="3" />
    <polygon points="14,13 22,17.5 14,22" />
  </svg>
</template>

<style lang="scss" scoped>
.flip-y {
  transform: scaleY(-1);
}
</style>
