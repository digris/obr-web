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
    const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
    const style = computed(() => {
      return {
        fill: "none",
        stroke: color.value,
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
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" :style="style">
    <circle stroke-width="3" cx="14" cy="24" r="3.5" />
    <circle stroke-width="3" cx="35" cy="12" r="3.5" />
    <circle stroke-width="3" cx="35" cy="36" r="3.5" />
    <line x1="17" y1="22" x2="32" y2="14" stroke-width="3" stroke-linecap="square" />
    <line x1="17" y1="26" x2="32" y2="34" stroke-width="3" stroke-linecap="square" />
  </svg>
</template>

<style lang="scss" scoped>
.flip-y {
  transform: scaleY(-1);
}
</style>
