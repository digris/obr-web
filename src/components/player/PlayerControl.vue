<script lang="ts">
import { defineComponent, computed } from "vue";
import type { PropType } from "vue";
import { useStore } from "vuex";
import { DateTime } from "luxon";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import eventBus from "@/eventBus";
import ButtonSkip from "./button/ButtonSkip.vue";
import ButtonPlay from "./button/ButtonPlay.vue";

const dt2hhmmss = (dt: any) => dt.toISOString().substr(11, 8);
const s2hhmmss = (s: number) => dt2hhmmss(new Date(s * 1000));

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
    const store = useStore();
    const { pause, resume: play } = usePlayerControls();
    const { isLive, isOndemand, isPlaying, isBuffering, currentTime, duration } = usePlayerState();

    const currentTimeDisplay = computed(() => {
      if (!currentTime.value) {
        return "00:00:00";
      }
      if (isLive.value) {
        const dt = DateTime.fromJSDate(currentTime.value);
        return dt.toLocaleString({
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        });
      }
      return s2hhmmss(currentTime.value);
    });

    const totalTimeDisplay = computed(() => {
      return duration.value ? s2hhmmss(duration.value) : "";
    });

    const hasPrevious = computed(() => store.getters["queue/previousIndex"] !== null);
    const hasNext = computed(() => store.getters["queue/nextIndex"] !== null);

    const playNext = () => {
      eventBus.emit("queue:controls:playNext");
    };

    const playPrevious = () => {
      eventBus.emit("queue:controls:playPrevious");
    };
    return {
      isLive,
      isOndemand,
      hasNext,
      hasPrevious,
      isPlaying,
      isBuffering,
      currentTime,
      duration,
      currentTimeDisplay,
      totalTimeDisplay,
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
      'is-ondemand': isOndemand,
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
      :outline-width="2"
      :outline-opacity="1"
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
  //align-items: center;
  //justify-content: center;
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
