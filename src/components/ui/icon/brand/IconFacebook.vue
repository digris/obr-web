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
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: props.color,
        stroke: "none",
        strokeWidth: (2 * BASE_SIZE) / props.size,
        strokeMiterlimit: 10,
        transform: `scale(${props.size / BASE_SIZE})`,
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
    viewBox="0 0 60 60"
    :style="style"
  >
    <path
      d="M37.7,29.9h-5v18h-7.5v-18h-3.6v-6.4h3.5v-4.1c0-3,1.4-7.5,7.5-7.5h5.5V18h-4c-0.8,0-1.6,0.6-1.6,1.4
	c0,0.1,0,0.2,0,0.3v3.7h5.7L37.7,29.9z"
    />
  </svg>
</template>
