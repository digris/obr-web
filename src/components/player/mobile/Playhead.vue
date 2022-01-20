<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import Progress from '../PlayheadProgress.vue';

const dt2hhmmss = (dt:any) => dt.toISOString().substr(11, 8);
const s2hhmmss = (s:number) => dt2hhmmss(new Date(s * 1000));

export default defineComponent({
  components: {
    Progress,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const store = useStore();
    const playerState = computed(() => store.getters['player/playerState']);
    const isLive = computed(() => playerState.value && playerState.value.isLive);
    const isPlaying = computed(() => playerState.value && playerState.value.isPlaying);
    const isBuffering = computed(() => playerState.value && playerState.value.isBuffering);
    const currentTime = computed(() => playerState.value && playerState.value.currentTime);
    const duration = computed(() => playerState.value && playerState.value.duration);
    const relPosition = computed(() => playerState.value && playerState.value.relPosition);

    const strCurrentTime = computed(() => {
      if (!currentTime.value) {
        return '00:00:00';
      }
      if (isLive.value) {
        const dt = DateTime.fromJSDate(currentTime.value);
        return dt.toLocaleString({
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
        });
      }
      return s2hhmmss(currentTime.value);
    });

    const strTotalTime = computed(() => {
      if (isLive.value) {
        return '';
      }
      if (!duration.value) {
        return '00:00:00';
      }
      return s2hhmmss(duration.value);
    });

    const hasPrevious = computed(() => store.getters['queue/previousIndex'] !== null);
    // const hasNext = computed(() => store.getters['queue/nextIndex'] !== null);
    const hasNext = ref(true);

    const pause = () => {
      eventBus.emit('player:controls', { do: 'pause' });
    };

    const play = () => {
      eventBus.emit('player:controls', { do: 'resume' });
    };

    const seek = (pos:number) => {
      const event = {
        do: 'seek',
        relPosition: pos,
      };
      eventBus.emit('player:controls', event);
    };

    const playNext = () => {
      eventBus.emit('queue:controls:playNext');
    };

    const playPrevious = () => {
      eventBus.emit('queue:controls:playPrevious');
    };

    return {
      isLive,
      isPlaying,
      isBuffering,
      currentTime,
      duration,
      relPosition,
      // times
      strCurrentTime,
      strTotalTime,
      // controls
      hasNext,
      hasPrevious,
      pause,
      play,
      seek,
      playNext,
      playPrevious,
    };
  },
});
</script>

<template>
  <div
    class="playhead"
    :class="{
      'is-disabled': disabled,
    }"
  >
    <div
      class="progress"
    >
      <div
        class="time time--current"
      >
        <span>{{ strCurrentTime }}</span>
      </div>
      <div
        class="time time--total"
      >
        <span>{{ strTotalTime }}</span>
      </div>
      <Progress
        :is-live="isLive"
        :is-playing="isPlaying"
        :is-buffering="isBuffering"
        :rel-position="relPosition"
        @seek="seek"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/base/typo";

.playhead {
  display: grid;
  width: 100%;
  min-height: 48px;
  .progress,
  .time {
    display: flex;
    align-items: center;
    transition: opacity 100ms;
  }
  .progress {
    position: relative;
    margin: 0 1rem;
    .time {
      @include typo.small;
      @include typo.bold;
      position: absolute;
      top: 0;
      display: flex;
      justify-content: center;
      padding: 0 1px;
      &--current {
        left: 0;
      }
      &--total {
        @include typo.dim;
        right: 0;
      }
    }
  }
  &.is-disabled {
    pointer-events: none;
    .progress {
      .time {
        opacity: 1;
      }
      .playhead-progress {
        opacity: 0.4;
      }
    }
  }
}
</style>
