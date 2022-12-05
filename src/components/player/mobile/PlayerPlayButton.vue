<script lang="ts">
import type { PropType } from "vue";
import { defineComponent } from "vue";

import { usePlayerControls, usePlayerState } from "@/composables/player";

import ButtonPlay from "../button/ButtonPlay.vue";

export default defineComponent({
  components: {
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
    const { isPlaying, isBuffering } = usePlayerState();
    return {
      isPlaying,
      isBuffering,
      pause,
      play,
    };
  },
});
</script>

<template>
  <div class="player-control">
    <ButtonPlay
      :is-playing="isPlaying"
      :is-buffering="isBuffering"
      :outlined="true"
      :outline-width="3"
      :outline-opacity="1"
      :base-color="fgColor"
      @pause="pause"
      @play="play"
    />
  </div>
</template>
