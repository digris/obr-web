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
  },
  setup(props) {
    const style = computed(() => {
      return {
        "--color": props.color,
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
  <div :style="style" class="buffering">
    <div class="bar bar--1" />
    <div class="bar bar--2" />
    <div class="bar bar--3" />
    <div class="bar bar--4" />
  </div>
</template>
<style lang="scss">
//TODO: how to implement keyframes / animations scoped?
@keyframes buffering {
  0% {
    height: 0%;
  }
  10% {
    height: 10%;
  }
  100% {
    height: 100%;
  }
}
</style>
<style lang="scss" scoped>
.buffering {
  display: grid;
  grid-column-gap: 3px;
  grid-template-columns: 3px 3px 3px 3px;
  align-items: center;
  width: 22px;
  height: 14px;

  .bar {
    width: 3px;
    height: 14px;
    background: var(--color);
    animation: buffering 1200ms infinite;
    &--1 {
      animation-delay: -800ms;
    }
    &--2 {
      animation-delay: -600ms;
    }
    &--3 {
      animation-delay: -400ms;
    }
    &--4 {
      animation-delay: -200ms;
    }
  }
}
</style>
