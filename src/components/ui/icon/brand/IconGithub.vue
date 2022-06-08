<script lang="ts">
import { defineComponent, computed } from "vue";

const BASE_SIZE = 60;

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
    height="60px"
    width="60px"
    viewBox="0 0 60 60"
    :style="style"
  >
    <!-- eslint-disable max-len -->
    <path
      d="M25.8,46c0,0,0-2.7,0-4.9c-5.8,1.3-7-2.5-7-2.5c-1-2.4-2.3-3-2.3-3c-1.9-1.3,0.1-1.3,0.1-1.3
	c2,0.1,3.2,2.2,3.2,2.2c1.8,3.2,4.8,2.3,6,1.7c0.2-1.3,0.8-2.3,1.3-2.8c-4.6-0.5-9.5-2.3-9.5-10.2c0-2.3,0.9-4.1,2.2-5.6
	c-0.2-0.5-1-2.7,0.2-5.5c0,0,1.7-0.5,5.7,2.2c1.6-0.4,3.4-0.6,5.2-0.8c1.7,0,3.6,0.2,5.2,0.8c4-2.7,5.7-2.2,5.7-2.2
	c1.2,2.9,0.4,4.9,0.2,5.5c1.3,1.5,2.2,3.3,2.2,5.6c0,8-4.8,9.8-9.5,10.2c0.8,0.6,1.4,1.9,1.4,3.9c0,2.3,0,6.8,0,6.8H25.8z"
    />
    <!-- eslint-enable max-len -->
  </svg>
</template>
