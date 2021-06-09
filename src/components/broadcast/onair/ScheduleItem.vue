<script lang="ts">
import { computed, defineComponent } from 'vue';
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import settings from '@/settings';
import LazyImage from '@/components/ui/LazyImage.vue';
import ScheduleItemPlay from './ScheduleItemPlay.vue';

export default defineComponent({
  components: {
    LazyImage,
    ScheduleItemPlay,
  },
  props: {
    hasFocus: {
      type: Boolean,
      default: false,
    },
    isCurrent: {
      type: Boolean,
      default: false,
    },
    scheduleItem: {
      type: Object,
      required: false,
      default: null,
    },
  },
  emits: [
    'play',
  ],
  setup(props, { emit }) {
    // eslint-disable-next-line arrow-body-style
    const isPlaceholder = computed(() => {
      return props.scheduleItem === null;
    });
    // eslint-disable-next-line arrow-body-style
    const media = computed(() => {
      return props.scheduleItem ? props.scheduleItem.media : null;
    });
    const release = computed(() => {
      if (media.value && media.value.releases.length) {
        return media.value.releases[0];
      }
      return null;
    });
    const image = computed(() => {
      return (release.value && release.value.image) ? release.value.image : null;
    });
    const timeFormat = DateTime.TIME_WITH_SECONDS;
    const streamUrl = computed(() => settings.STREAM_ENDPOINTS.dash);
    const play = () => {
      let startTime = -10;
      if (props.isCurrent) {
        startTime = -10;
      } else {
        const now = DateTime.now();
        const { timeStart } = props.scheduleItem;
        const diffDt = timeStart.diff(now, 'seconds');
        const diffSeconds = diffDt.seconds;
        console.dir({
          now,
          timeStart,
          diffDt,
          diffSeconds,
        });
        console.debug('diff', diffSeconds);
        startTime = diffSeconds + 10;
        // startTime = timeStart.diff(now, 'seconds').seconds;
      }
      const event = {
        do: 'play',
        url: `${streamUrl.value}?${Date.now()}`,
        startTime,
      };
      eventBus.emit('player:controls', event);
      emit('play');
    };
    return {
      isPlaceholder,
      media,
      release,
      image,
      timeFormat,
      play,
    };
  },
});
</script>

<template>
  <div
    class="schedule-item"
    :class="{'has-focus': hasFocus, 'is-placeholder': isPlaceholder}"
  >
    <div
      v-if="isPlaceholder"
      class="panel"
    >
      (( placeholder ))
    </div>
    <div
      v-else
      class="panel"
    >
      <LazyImage
        :image="image"
      />
      <div
        v-if="scheduleItem"
        class="info"
      >
        <div
          class="meta"
        >
          {{ scheduleItem.media.name }}
        </div>
        <div
          class="timing"
        >
          {{ scheduleItem.timeStart.toLocaleString(timeFormat) }}
          -
          {{ scheduleItem.timeEnd.toLocaleString(timeFormat) }}
        </div>
      </div>
    </div>
    <div
      class="actions"
    >
      <ScheduleItemPlay
        :is-current="isCurrent"
        :item="scheduleItem"
        @play="play"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
@use "@/style/base/typo";
.schedule-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(var(--c-black));
  &.is-placeholder {
    background: rgb(var(--c-black));
  }
  .panel {
    width: 100%;
    height: 100%;
  }
  .info {
    position: absolute;
    bottom: 0;
    .meta {
      @include typo.small;
      padding: 0.25rem;
      color: black;
      background: white;
    }
    .timing {
      @include typo.small;
      padding: 0.25rem;
      color: black;
      background: white;
    }
  }
  .actions {
    position: absolute;
  }
  /*
  &:not(.has-focus) {
    .actions {
      left: 0;
      transform: scale(0.5);
    }
  }
  */
}
</style>
