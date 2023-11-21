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
      default: "--c-dark",
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
    const style = computed(() => {
      return {
        "--color": color.value,
        transform: `scale(${props.scale})`,
      };
    });
    return {
      color,
      style,
      size,
    };
  },
});
</script>

<template>
  <div
    class="playing-container"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
    }"
  >
    <div :style="style" class="playing">
      <div class="bar bar--1" />
      <div class="bar bar--2" />
      <div class="bar bar--3" />
      <div class="bar bar--4" />
    </div>
  </div>
</template>
<style lang="scss">
// TODO: how to implement keyframes / animations scoped?
@keyframes eq {
  0%,
  80%,
  100% {
    height: 50%;
  }

  35% {
    height: 100%;
  }

  50% {
    height: 70%;
  }

  /* stylelint-disable-next-line keyframe-block-no-duplicate-selectors */
  80% {
    height: 80%;
  }
}
</style>
<style lang="scss" scoped>
.playing-container {
  display: grid;
  align-items: center;
  justify-content: center;
}

.playing {
  height: 14px;
  width: 22px;
  display: grid;
  grid-column-gap: 3px;
  grid-template-columns: 3px 3px 3px 3px;
  align-items: flex-end;

  .bar {
    height: 10px;
    width: 3px;
    background: var(--color);
    transition: height 200ms;
    animation: eq 1200ms infinite;

    &--1 {
      animation-delay: -550ms;
    }

    &--2 {
      transition: opacity 100ms;
      animation-delay: -700ms;
    }

    &--3 {
      animation-delay: -350ms;
    }
  }
}
</style>
