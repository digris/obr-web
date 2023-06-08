<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";

import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueControls, useQueueState } from "@/composables/queue";

import ButtonPlay from "../button/ButtonPlay.vue";
import ButtonSkip from "../button/ButtonSkip.vue";

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
    const { isLive, isPlaying, isBuffering } = usePlayerState();
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
      playNext,
      playPrevious,
      pause,
      play,
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
      <ButtonSkip
        :scale="1"
        :outlined="true"
        :rotate="180"
        :disabled="!hasPrevious"
        @click.prevent="playPrevious"
      />
    </div>
    <ButtonPlay
      :is-playing="isPlaying"
      :is-buffering="isBuffering"
      :outlined="true"
      :outline-width="3"
      outline-opacity="100%"
      :base-color="fgColor"
      :scale="1.25"
      @pause="pause"
      @play="play"
    />
    <div class="right">
      <ButtonSkip :scale="1" :outlined="true" :disabled="!hasNext" @click.prevent="playNext" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.player-control {
  display: flex;
  column-gap: 1rem;

  .left,
  .right {
    display: flex;
    align-items: center;
    transition: opacity 500ms;
  }

  &.is-live {
    .left,
    .right {
      opacity: 0;
    }
  }
}
</style>
