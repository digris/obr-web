<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useElementSize, useMouseInElement } from "@vueuse/core";
import { round } from "lodash-es";

import PlayheadHandle from "@/components/player/PlayheadHandle.vue";
import PlayheadTime from "@/components/player/PlayheadTime.vue";
import { usePlayerState } from "@/composables/player";

export default defineComponent({
  components: {
    PlayheadHandle,
    PlayheadTime,
  },
  emits: ["seek"],
  setup(props, { emit }) {
    const root = ref<HTMLElement | null>(null);
    // const isHover = ref(false);
    const { x: mouseX, isOutside } = useMouseInElement(root);
    const { width } = useElementSize(root);
    const {
      isLive,
      isOndemand,
      isPlaying,
      isBuffering,
      relPosition: position,
      media,
      duration,
    } = usePlayerState();
    const isHover = computed(() => {
      return !isOutside.value;
    });
    const playheadTime = computed(() => {
      if (isOutside.value) {
        return null;
      }
      return (duration.value * mouseX.value) / width.value;
    });
    const playheadTimeX = computed(() => {
      if (isOutside.value) {
        return null;
      }
      // dom element is 60px wide
      const posX = mouseX.value - 36;
      return Math.max(Math.min(posX, width.value - 66), 6);
    });
    const playheadHandleX = computed(() => {
      if (isOutside.value) {
        return null;
      }
      // dom element is 20px wide
      const posX = width.value * position.value - 10;
      return Math.max(Math.min(posX, width.value - 20), 0);
    });
    const cueIn = computed(() => {
      if (media.value?.cueIn && duration.value) {
        return round(media.value?.cueIn / duration.value, 3);
      }
      return 0;
    });
    const cueOut = computed(() => {
      if (media.value?.cueOut && duration.value) {
        return 1 - round(media.value?.cueOut / duration.value, 3);
      }
      return 1;
    });
    const seek = (e: PointerEvent) => {
      if (isLive.value) {
        console.warn("no seek in live mode!");
        return;
      }
      if (!root.value) {
        return 0;
      }
      // const seekTo = e.offsetX / root.value.getBoundingClientRect().width;
      const seekTo = e.offsetX / width.value;
      emit("seek", seekTo);
    };
    return {
      root,
      isHover,
      playheadTime,
      playheadTimeX,
      playheadHandleX,
      mouseX,
      isLive,
      isOndemand,
      isPlaying,
      isBuffering,
      position,
      cueIn,
      cueOut,
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
      'is-hover': isHover,
      'is-live': isLive,
      'is-ondemand': isOndemand,
      'is-playing': isPlaying,
      'is-buffering': isBuffering,
    }"
  >
    <svg viewBox="0 0 1000 32" preserveAspectRatio="none" fill="transparent" @click="seek">
      <rect x="0" y="0" width="100%" height="32" />
      <rect x="0" y="14" width="100%" height="4" class="progress-total" />
      <g v-if="isOndemand">
        <rect
          v-if="position"
          x="0"
          y="14"
          :width="`${position * 100}%`"
          height="4"
          class="progress-position"
        />
        <rect v-if="cueIn" y="10" :x="`${cueIn * 100}%`" width="1" height="10" class="cue-point" />
        <rect
          v-if="cueOut"
          y="10"
          :x="`${cueOut * 100}%`"
          width="1"
          height="10"
          class="cue-point"
        />
      </g>
      <g v-else>
        <rect x="0" y="14" width="100%" height="1" class="progress-placeholder" />
      </g>
    </svg>
    <PlayheadHandle
      v-if="isOndemand"
      :is-visible="isHover"
      :style="{ left: `${playheadHandleX}px` }"
    />
    <PlayheadTime v-if="isOndemand" :time="playheadTime" :style="{ left: `${playheadTimeX}px` }" />
  </div>
</template>

<style lang="scss" scoped>
.playhead-progress {
  position: relative;
  height: 32px;
  width: 100%;

  svg {
    height: 32px;
    width: 100%;
  }

  .progress-total {
    transition: fill 100ms;
    fill: rgb(var(--c-fg) 0.2);
  }

  .progress-position {
    // NOTE: width transition duration equals audioPlayer's POLL_INTERVAL
    transition: fill 100ms, width 100ms linear;
    fill: rgb(var(--c-fg) 0.5);
  }

  .progress-placeholder {
    fill: rgb(var(--c-fg) 0.2);
  }

  .cue-point {
    fill: rgb(var(--c-fg) 1);
  }

  &.is-buffering {
    svg {
      cursor: wait;
    }
  }

  &.is-hover {
    .progress-position {
      fill: rgb(var(--c-fg) 1);
    }
  }

  &.is-ondemand {
    svg {
      cursor: pointer;
    }
  }

  &.is-live {
    .progress-total {
      fill: rgb(var(--c-fg) 0);
    }
  }
}

.playhead-handle {
  top: 5px;
  position: absolute;
  pointer-events: none;
  transition: left 100ms linear;
}

.playhead-time {
  top: -13px;
  position: absolute;
  pointer-events: none;
}
</style>
