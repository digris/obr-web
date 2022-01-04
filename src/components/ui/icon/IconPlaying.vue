<script lang="ts">
import { computed, defineComponent } from 'vue';

const BASE_SIZE = 48;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    color: {
      type: String,
      default: 'rgb(var(--c-page-bg))',
    },
    pause: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        '--color': props.color,
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
  <div
    :style="style"
    class="playing"
    :class="{
      pause: pause,
    }"
  >
    <div
      class="bar bar--1"
    />
    <div
      class="bar bar--2"
    />
    <div
      class="bar bar--3"
    />
  </div>
</template>
<style lang="scss">
//TODO: how to implement keyframes / animations scoped?
@keyframes eq {
  0%, 80%, 100% {
    height: 50%;
  }
  35% {
    height: 100%;
  }
  50% {
    height: 70%;
  }
  80% {
    height: 80%;
  }
}
</style>
<style lang="scss" scoped>
.playing {
  display: grid;
  grid-column-gap: 2px;
  grid-template-columns: 4px 4px 4px;
  align-items: flex-end;
  width: 16px;
  height: 14px;

  &.pause {
    .bar {
      animation: unset;
      height: 100%;
      &--2 {
        opacity: 0;
      }
    }
  }

  .bar {
    width: 4px;
    height: 10px;
    background: var(--color);
    animation: eq 1200ms infinite;
    transition: height 200ms;
    &--1 {
      animation-delay: -550ms;
    }
    &--2 {
      animation-delay: -700ms;
      transition: opacity 100ms;
    }
    &--3 {
      animation-delay: -350ms;
    }
  }
}
</style>
