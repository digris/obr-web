<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  props: {
    isLive: {
      type: Boolean,
      default: false,
    },
    isPlaying: {
      type: Boolean,
      default: false,
    },
    isBuffering: {
      type: Boolean,
      default: false,
    },
    relPosition: {
      type: Number,
    },
    relCueIn: {
      type: Number,
      default: 0,
    },
    relCueOut: {
      type: Number,
      default: 100,
    },
  },
  emits: ["seek"],
  setup(props, { emit }) {
    const root = ref<HTMLElement | null>(null);
    const seek = (e: PointerEvent) => {
      if (props.isLive) {
        console.warn("no seek in live mode!");
        return;
      }
      if (!root.value) {
        return 0;
      }
      const relPosition = e.offsetX / root.value.getBoundingClientRect().width;
      emit("seek", relPosition);
    };
    return {
      root,
      seek,
    };
  },
});
</script>

<template>
  <div
    ref="root"
    class="playhead-progress"
    :class="{
      'is-live': isLive,
      'is-playing': isPlaying,
      'is-buffering': isBuffering,
    }"
  >
    <svg viewBox="0 0 1000 32" preserveAspectRatio="none" fill="transparent" @click="seek">
      <rect x="0" y="0" width="100%" height="32" />
      <rect x="0" y="12" width="100%" height="8" class="progress-total" />
      <rect
        v-if="relPosition"
        x="0"
        y="12"
        :width="`${relPosition * 100}%`"
        height="8"
        class="progress-position"
      />
      <rect
        v-if="relCueIn || relCueOut"
        y="18"
        :x="`${relCueIn * 100}%`"
        :width="`${(relCueOut - relCueIn) * 100}%`"
        height="2"
        class="cue-area"
      />
    </svg>
  </div>
</template>

<style lang="scss" scoped>
.playhead-progress {
  width: 100%;
  height: 32px;
  svg {
    width: 100%;
    height: 32px;
    cursor: pointer;
  }
  .progress-total {
    transition: fill 100ms;
    fill: rgba(var(--c-fg), 0.2);
  }
  .progress-position {
    fill: rgba(var(--c-fg), 1);
  }
  .cue-area {
    fill: rgba(var(--c-fg), 0.8);
  }
  &.is-buffering {
    svg {
      cursor: wait;
    }
  }
  &.is-live {
    svg {
      cursor: not-allowed;
    }
    .progress-total {
      fill: rgba(var(--c-fg), 0.2);
    }
  }
}
</style>
