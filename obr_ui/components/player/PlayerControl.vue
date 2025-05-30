<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";

import { useAnalytics } from "@/composables/analytics";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueControls, useQueueState } from "@/composables/queue";
import { s2hhmmss } from "@/utils/time";

import ButtonPlay from "./button/ButtonPlay.vue";
import ButtonSkip from "./button/ButtonSkip.vue";

export default defineComponent({
  components: {
    ButtonSkip,
    ButtonPlay,
  },
  props: {
    fgColor: {
      type: Array as PropType<Array<number>>,
      default: () => [0, 0, 0],
    },
  },
  setup() {
    const { pause, resume: play } = usePlayerControls();
    const { isLive, isPlaying, isBuffering, currentTime, duration } = usePlayerState();
    const { logUIEvent } = useAnalytics();
    const logFn = <T extends (...args: any[]) => any>(
      fn: T,
      event: string
    ): ((...args: Parameters<T>) => ReturnType<T>) => {
      return (...args: Parameters<T>) => {
        const result = fn(...args);
        logUIEvent(event);
        return result;
      };
    };
    const currentTimeDisplay = computed(() => {
      if (currentTime.value === null) {
        return "00:00:00";
      }
      return s2hhmmss(currentTime.value);
    });
    const totalTimeDisplay = computed(() => (duration.value ? s2hhmmss(duration.value) : ""));
    const { previousIndex, nextIndex } = useQueueState();
    const { playPrevious, playNext } = useQueueControls();
    const hasPrevious = computed(() => previousIndex.value !== null);
    const hasNext = computed(() => nextIndex.value !== null);
    return {
      isLive,
      hasNext,
      hasPrevious,
      isPlaying,
      isBuffering,
      currentTimeDisplay,
      totalTimeDisplay,
      play,
      pause,
      playNext: logFn(playNext, "player:play-next"),
      playPrevious: logFn(playPrevious, "player:play-previous"),
    };
  },
});
</script>

<template>
  <div
    class="player-control"
    :class="{
      'is-live': isLive,
    }"
  >
    <div class="left">
      <div class="time" v-text="currentTimeDisplay" />
      <ButtonSkip :rotate="180" :disabled="!hasPrevious" @click.prevent="playPrevious" />
    </div>
    <ButtonPlay
      :is-playing="isPlaying"
      :is-buffering="isBuffering"
      :outlined="true"
      :outline-width="3"
      outline-opacity="100%"
      :base-color="fgColor"
      @pause="pause"
      @play="play"
    />
    <div class="right">
      <ButtonSkip :disabled="!hasNext" @click.prevent="playNext" />
      <div class="time" v-text="totalTimeDisplay" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.player-control {
  display: flex;

  .left,
  .right {
    display: flex;
    align-items: center;
    transition: opacity 500ms;
  }

  .time {
    @include typo.small;

    margin: 0 0.5rem;
    width: 54px;
    overflow: hidden;
  }

  &.is-live {
    .left,
    .right {
      opacity: 0;
    }
  }
}
</style>
