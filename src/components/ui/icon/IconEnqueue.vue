<script lang="ts">
import { defineComponent, computed } from "vue";

const BASE_SIZE = 48;

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
    flipY: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const size = computed(() => {
      return props.size || BASE_SIZE;
    });
    const style = computed(() => {
      return {
        fill: props.color,
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
