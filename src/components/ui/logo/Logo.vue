<script lang="ts">
import { computed, defineComponent } from "vue";

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 48,
    },
    color: {
      type: String,
      default: "rgb(var(--c-page-fg) / 100%)",
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: "none",
        stroke: props.color,
        strokeWidth: (24 * BASE_SIZE) / props.size,
        strokeMiterlimit: 10,
        // transform: `scale(${props.size / BASE_SIZE})`,
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
    viewBox="0 0 602 602"
    :width="size"
    :height="size"
    :style="style"
    class="logo"
  >
    <polygon points="539 301 138 486.99 138 115.01 539 301" />
    <rect x="138.01" y="107" width="119.01" height="387.98" />
    <rect x="345.01" y="106.99" width="119.01" height="387.98" />
    <circle cx="301" cy="301" r="287" />
  </svg>
</template>
