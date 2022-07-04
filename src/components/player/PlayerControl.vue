<script lang="ts">
import { defineComponent, computed } from "vue";
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
    isLive: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const store = useStore();
    const { pause, resume: play } = usePlayerControls();
    const { isPlaying, isBuffering, currentTime, duration } = usePlayerState();

    const currentTimeDisplay = computed(() => {
      if (!currentTime.value) {
        return "00:00:00";
      }
      if (props.isLive) {
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
      if (props.isLive) {
        return "--:--:--";
      }
      return s2hhmmss(duration.value);
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
  <div class="player-control">
    <div class="time">
      {{ currentTimeDisplay }}
    </div>
    <ButtonSkip :size="48" :rotate="180" :disabled="!hasPrevious" @click.prevent="playPrevious" />
    <ButtonPlay
      :is-playing="isPlaying"
      :is-buffering="isBuffering"
      :outline-width="2"
      :outline-opacity="1"
      @pause="pause"
      @play="play"
    />
    <ButtonSkip :size="48" :disabled="!hasNext" @click.prevent="playNext" />
    <div class="time">
      {{ totalTimeDisplay }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.player-control {
  display: grid;
  grid-template-columns: auto 48px 48px 48px auto;
  grid-column-gap: 0.5rem;
  align-items: center;
  .time {
    @include typo.small;
  }
}
</style>
