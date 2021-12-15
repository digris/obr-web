<script lang="ts">
import { ref, computed, defineComponent } from 'vue';

const BASE_SIZE = 160;

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    filled: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    outlineWidth: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: '--c-page-fg',
    },
    fillColorVar: {
      type: String,
      default: '--c-page-fg-inverse',
    },
    progress: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const root = ref(null);
    const radius = computed(() => {
      return (BASE_SIZE - 8 - props.outlineWidth) * 0.5;
    });
    const scale = computed(() => {
      return BASE_SIZE / props.size;
    });
    const segment = computed(() => {
      if (!props.progress) {
        return 1000;
      }
      return radius.value * Math.PI * 2 * props.progress;
    });
    const style = computed(() => {
      return {
        strokeWidth: (3 * BASE_SIZE) / props.size,
        '--size': `${props.size}px`,
        '--outline-width': `${props.outlineWidth}px`,
        '--stroke-width': `${props.outlineWidth * scale.value}px`,
        '--color-var': `var(${props.colorVar})`,
      };
    });
    const cursorPosition = ref(0);
    const onMousemove = (e: MouseEvent) => {
      // @ts-ignore
      const x = e.clientX - root.value.offsetLeft - (props.size * 0.5);
      // @ts-ignore
      const y = e.clientY - root.value.offsetTop - (props.size * 0.5);
      const point = {
        // x,
        // y,
        p: (Math.atan2(y, x) * 180) / Math.PI,
      };
      console.debug(point);
      cursorPosition.value = point.p;
    };
    return {
      root,
      style,
      radius,
      segment,
      onMousemove,
      cursorPosition,
    };
  },
});
</script>

<template>
  <div
    class="circle-progress-button"
    :style="style"
    ref="root"
  >
    <div
      class="inner"
    >
      <slot
        name="default"
      />
    </div>
    <svg
      class="circle"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 160 160"
    >
      <circle
        class="ring ring--full"
        cx="80"
        cy="80"
        :r="radius"
        :style="{
          stroke: 'rgb(var(--c-page-fg))',
        }"
      />
      <!--
      <circle
        class="ring ring--current"
        cx="80"
        cy="80"
        :r="radius"
        :style="{
          stroke: 'rgb(var(--c-page-fg-inverse))',
          strokeDasharray: `${segment} 1000`,
        }"
      />
      -->
      <!--
      <circle
        class="ring ring--current"
        cx="80"
        cy="80"
        @mousemove="onMousemove"
        :r="radius"
        :style="{
          stroke: '#ff00ff',
          strokeDasharray: `${segment * 1.5} 1000`,
        }"
      />
      -->
    </svg>
    <div
      v-if="filled"
      class="fill"
    >
      <div
        class="fill__inner"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.circle-progress-button {
  position: relative;
  display: inline-flex;
  width: var(--size);
  height: var(--size);
  transition: background 200ms;
  border-radius: 50%;
  &:hover {
    background: rgba(var(--c-page-fg), 0.1);
  }
  .circle {
    position: absolute;
    top: 0;
    transform: rotate(-90deg);
    .ring {
      fill: none;
      stroke-width: var(--stroke-width);
      &--current {
        stroke-width: calc(var(--stroke-width) * 0.25);
      }
    }
  }
  .inner {
    display: flex;
    overflow: hidden;
    position: absolute;
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }
  .fill {
    width: 100%;
    height: 100%;
    padding: var(--outline-width);
    &__inner {
      width: 100%;
      height: 100%;
      //background: red;
      background: rgb(var(--color-var));
      border-radius: 100%;
    }
  }
}
</style>
