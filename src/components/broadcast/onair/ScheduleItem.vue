<script lang="ts">
import { computed, defineComponent } from 'vue';
// import { useStore } from 'vuex';
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import { playStream } from '@/player/stream';
import LazyImage from '@/components/ui/LazyImage.vue';
import { requireSubscription } from '@/utils/account';
import PlayButton from './button/Play.vue';

export default defineComponent({
  components: {
    LazyImage,
    PlayButton,
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
    // const store = useStore();
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
    // eslint-disable-next-line @typescript-eslint/no-shadow
    const playMedia = requireSubscription((media: object) => {
      const payload = {
        media: [media],
      };
      eventBus.emit('queue:controls:enqueue', payload);
    }, 'foo');
    const play = () => {
      if (props.isCurrent) {
        const startTime = -10;
        playStream(startTime);
        emit('play');
      } else {
        playMedia(props.scheduleItem.media);
      }
      // let startTime = -10;
      // if (!props.isCurrent) {
      //   const now = DateTime.now();
      //   const { timeStart } = props.scheduleItem;
      //   const diffDt = timeStart.diff(now, 'seconds');
      //   const diffSeconds = diffDt.seconds;
      //   startTime = diffSeconds + 10;
      // }
      // playStream(startTime);
      // emit('play');
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
      <PlayButton
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
    //crop a couple of pixels
    overflow: hidden;
    :deep(img) {
      transform: scale(1.02);
      //transform: scale(0.95);
    }
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
