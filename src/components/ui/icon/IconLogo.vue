<script lang="ts">
import { defineComponent, computed } from "vue";
import { useIconSize } from "@/composables/icon";

enum Mode {
  default = "default",
  play = "play",
  pause = "pause",
  playing = "playing",
}

export default defineComponent({
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    outlineWidth: {
      type: Number,
      default: 2.25,
    },
    colorVar: {
      type: String,
      default: "--c-fg",
    },
    mode: {
      type: String,
      default: Mode.default,
    },
  },
  setup(props) {
    const { iconSize: size } = useIconSize(props.scale);
    const color = computed(() => `rgb(var(${props.colorVar}))`);
    const style = computed(() => {
      // const mode: Mode = Mode[props.mode as keyof typeof Mode];
      return {
        fill: "none",
        stroke: color.value,
        // NOTE: add strokeWidth calculations
        strokeWidth: props.outlineWidth,
        strokeMiterlimit: 10,
        width: `${size.value}px`,
        height: `${size.value}px`,
      };
    });
    return {
      style,
      Mode,
    };
  },
});
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    height="48px"
    width="48px"
    viewBox="0 0 48 48"
    :style="style"
  >
    <!-- eslint-disable max-len -->
    <transition name="icon">
      <g v-if="mode === Mode.default">
        <polygon points="43.902439 24 10.369338 39.554007 10.369338 8.44599303" />
        <rect x="10.369338" y="7.77700348" width="9.95121951" height="32.445993" />
        <rect x="27.6794425" y="7.77700348" width="9.95121951" height="32.445993" />
      </g>
      <g v-else-if="mode === Mode.play">
        <polyline
          points="20.3205575 34.9379791 20.3205575 40.2229965 10.369338 40.2229965 10.369338 7.77700348 20.3205575 7.77700348 20.3205575 12.6940767"
        />
        <polyline
          points="37.630662 26.9101045 37.630662 40.2229965 27.6794425 40.2229965 27.6794425 31.9275261"
        />
        <polyline
          points="27.6794425 16.4738676 27.6794425 7.77700348 37.630662 7.77700348 37.630662 21.0898955"
        />
        <polygon points="43.902439 24 10.369338 39.554007 10.369338 8.44599303" />
      </g>
      <g v-else-if="mode === Mode.pause">
        <line x1="27.6794425" y1="31.5261324" x2="20.3205575" y2="34.9379791" />
        <polyline points="37.630662 21.0898955 43.902439 24 37.630662 26.9101045" />
        <line x1="20.3205575" y1="13.0620209" x2="27.4452962" y2="16.3651568" />
        <rect x="10.369338" y="7.77700348" width="9.95121951" height="32.445993" />
        <rect x="27.6794425" y="7.77700348" width="9.95121951" height="32.445993" />
      </g>
      <g v-else-if="mode === Mode.playing" class="playing">
        <!--
        <rect class="playing--left" x="10.369338" y="26.7930314" width="9.95121951" height="13.4299652" />
        <rect class="playing--right" x="27.6794425" y="10.9379791" width="9.95121951" height="29.2850174" />
        -->
        <rect
          class="playing--right"
          x="10.369338"
          y="7.77700348"
          width="9.95121951"
          height="32.445993"
        />
        <rect
          class="playing--left"
          x="27.6794425"
          y="7.77700348"
          width="9.95121951"
          height="32.445993"
        />
      </g>
    </transition>
    <!-- eslint-enable max-len -->
  </svg>
</template>

<style lang="scss">
//TODO: how to implement keyframes / animations scoped?
@keyframes eq-left {
  0%,
  100% {
    height: 14px;
  }
  10% {
    height: 32px;
  }
  20% {
    height: 26px;
  }
  30% {
    height: 32px;
  }
  40% {
    height: 20px;
  }
  50% {
    height: 30px;
  }
  60% {
    height: 22px;
  }
  70% {
    height: 26px;
  }
  82% {
    height: 20px;
  }
  90% {
    height: 30px;
  }
}
</style>

<style lang="scss" scoped>
svg {
  &:hover {
    background: transparent;
  }
  .playing {
    transform: rotate(180deg);
    transform-origin: center;
    &--left {
      animation: eq-left 2000ms infinite;
      animation-timing-function: ease-in-out;
    }
    &--right {
      animation: eq-left 2000ms infinite;
      animation-timing-function: linear;
      animation-delay: 20ms;
    }
  }
}

.icon-enter-active,
.icon-leave-active {
  opacity: 1;
  transition: opacity 20ms ease-in-out;
}

.icon-enter,
.icon-leave-to {
  opacity: 0;
}
</style>
