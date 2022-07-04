<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useMouseInElement, useElementSize } from "@vueuse/core";
import { usePlayerState } from "@/composables/player";
import PlayheadHandle from "@/components/player/PlayheadHandle.vue";
import PlayheadTime from "@/components/player/PlayheadTime.vue";

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
      isPlaying,
      isBuffering,
      relPosition: position,
      currentMedia: media,
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
      return media.value?.cueIn / duration.value;
    });
    const cueOut = computed(() => {
      return 1 - media.value?.cueOut / duration.value;
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
      'is-playing': isPlaying,
      'is-buffering': isBuffering,
    }"
  >
    <svg viewBox="0 0 1000 32" preserveAspectRatio="none" fill="transparent" @click="seek">
      <rect x="0" y="0" width="100%" height="32" />
      <rect x="0" y="14" width="100%" height="4" class="progress-total" />
      <rect
        v-if="position"
        x="0"
        y="14"
        :width="`${position * 100}%`"
        height="4"
        class="progress-position"
      />
      <rect v-if="cueIn" y="16" :x="`${cueIn * 100}%`" width="2" height="10" class="cue-point" />
      <rect v-if="cueOut" y="16" :x="`${cueOut * 100}%`" width="1" height="10" class="cue-point" />
    </svg>
    <PlayheadHandle :is-visible="isHover" :style="{ left: `${playheadHandleX}px` }" />
    <PlayheadTime :time="playheadTime" :style="{ left: `${playheadTimeX}px` }" />
  </div>
</template>

<style lang="scss" scoped>
.playhead-progress {
  position: relative;
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
    transition: fill 100ms;
    fill: rgba(var(--c-fg), 0.5);
  }
  .cue-point {
    fill: rgba(var(--c-fg), 1);
  }
  &.is-buffering {
    svg {
      cursor: wait;
    }
  }
  &.is-hover {
    .progress-position {
      fill: rgba(var(--c-fg), 1);
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
.playhead-handle {
  pointer-events: none;
  position: absolute;
  top: 5px;
}
.playhead-time {
  pointer-events: none;
  position: absolute;
  top: -13px;
}
</style>
