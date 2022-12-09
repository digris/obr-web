<script lang="ts">
import { computed, defineComponent } from "vue";

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
    const color = computed(() => `rgb(var(${props.colorVar}) / 100%)`);
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
        <g class="playing--left">
          <polyline
            stroke-linecap="square"
            points="13.8525 35.7369231 15.505543 35.7369231 16.8375 35.7369231"
          />
          <polyline
            stroke-linecap="square"
            points="13.8525 31.7430769 15.505543 31.7430769 16.8375 31.7430769"
          />
          <polyline
            stroke-linecap="square"
            points="13.8525 27.7492308 15.505543 27.7492308 16.8375 27.7492308"
          />
          <polyline
            stroke-linecap="square"
            points="13.8525 23.7553846 15.505543 23.7553846 16.8375 23.7553846"
          />
          <polyline
            stroke-linecap="square"
            points="13.8525 19.7615385 15.505543 19.7615385 16.8375 19.7615385"
          />
          <polyline
            stroke-linecap="square"
            points="13.8525 15.7676923 15.505543 15.7676923 16.8375 15.7676923"
          />
          <polyline
            stroke-linecap="square"
            points="13.8525 11.7738462 15.505543 11.7738462 16.8375 11.7738462"
          />
        </g>
        <rect x="10.37" y="7.78" width="9.95" height="32.45"></rect>
        <g class="playing--right">
          <polyline
            stroke-linecap="square"
            points="31.1625 35.7369231 32.815543 35.7369231 34.1475 35.7369231"
          />
          <polyline
            stroke-linecap="square"
            points="31.1625 31.7430769 32.815543 31.7430769 34.1475 31.7430769"
          />
          <polyline
            stroke-linecap="square"
            points="31.1625 27.7492308 32.815543 27.7492308 34.1475 27.7492308"
          />
          <polyline
            stroke-linecap="square"
            points="31.1625 23.7553846 32.815543 23.7553846 34.1475 23.7553846"
          />
          <polyline
            stroke-linecap="square"
            points="31.1625 19.7615385 32.815543 19.7615385 34.1475 19.7615385"
          />
          <polyline
            stroke-linecap="square"
            points="31.1625 15.7676923 32.815543 15.7676923 34.1475 15.7676923"
          />
          <polyline
            stroke-linecap="square"
            points="31.1625 11.7738462 32.815543 11.7738462 34.1475 11.7738462"
          />
        </g>
        <rect x="27.68" y="7.78" width="9.95" height="32.45" />
      </g>
    </transition>
    <!-- eslint-enable max-len -->
  </svg>
</template>

<style lang="scss">
// TODO: how to implement keyframes / animations scoped?
@keyframes eq-bars-7 {
  0%,
  100% {
    opacity: 1;
  }

  15%,
  70% {
    opacity: 0;
  }
}
@keyframes eq-bars-6 {
  0%,
  100% {
    opacity: 1;
  }

  25%,
  70% {
    opacity: 0;
  }
}
@keyframes eq-bars-5 {
  0%,
  100% {
    opacity: 1;
  }

  30%,
  70% {
    opacity: 0;
  }
}
@keyframes eq-bars-4 {
  0%,
  100% {
    opacity: 1;
  }

  40%,
  60% {
    opacity: 0;
  }
}
@keyframes eq-bars-3 {
  0%,
  100% {
    opacity: 1;
  }

  45%,
  55% {
    opacity: 0;
  }
}
</style>

<style lang="scss" scoped>
svg {
  &:hover {
    background: transparent;
  }

  .playing {
    polyline {
      stroke-width: 2.5;
    }

    &--left,
    &--right {
      :nth-child(7) {
        animation: eq-bars-7 800ms infinite;
      }

      :nth-child(6) {
        animation: eq-bars-6 800ms infinite;
      }

      :nth-child(5) {
        animation: eq-bars-5 800ms infinite;
      }

      :nth-child(4) {
        animation: eq-bars-4 800ms infinite;
      }

      :nth-child(3) {
        animation: eq-bars-3 800ms infinite;
      }

      :nth-child(2) {
        animation: eq-bars-2 800ms infinite;
      }

      :nth-child(1) {
        animation: eq-bars-1 800ms infinite;
      }
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
