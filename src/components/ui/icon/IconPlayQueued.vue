<script lang="ts">
import { computed, defineComponent } from "vue";

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: "rgb(var(--c-page-bg))",
    },
    // marked: {
    //   type: Boolean,
    //   default: false,
    // },
  },
  setup(props) {
    const style = computed(() => {
      return {
        fill: "none",
        stroke: "none",
        // stroke: props.color,
        strokeWidth: 2.5,
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
  <!--
  <pre
    v-text="style"
  />
  -->
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <polygon :stroke="color" points="34.7,24 22,30.4 22,17.6" />
    <polygon :fill="color" points="18.2,30.8 18.2,17.2 18.2,14.4 15.8,13.1 15.8,34.9 18.2,33.6" />
  </svg>
</template>
