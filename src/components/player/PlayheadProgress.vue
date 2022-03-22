<script>
export default {
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
  },
  methods: {
    seek(e) {
      if (this.isLive) {
        console.warn("no seek in live mode!");
        return;
      }
      const relPosition = e.offsetX / this.$el.getBoundingClientRect().width;
      this.$emit("seek", relPosition);
    },
  },
};
</script>

<template>
  <div
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
