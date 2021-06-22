<script lang="ts">
import {
  computed,
  ref,
  reactive,
  watch,
} from 'vue';
import { useStore } from 'vuex';

import StationTime from '@/components/broadcast/onair/StationTime.vue';
import ScheduleItem from '@/components/broadcast/onair/ScheduleItem.vue';

export default {
  components: {
    StationTime,
    ScheduleItem,
  },
  setup() {
    const store = useStore();
    const viewport = computed(() => store.getters['ui/viewport']);
    const current = computed(() => store.getters['schedule/current']);
    const next = computed(() => store.getters['schedule/next']);
    const past = computed(() => store.getters['schedule/past']);
    const items = computed(() => [next.value || null, current.value || null, ...past.value]);
    const itemSize = computed(() => {
      const { width, height } = viewport.value;
      const innerWidth = width - 60 * 2;
      const innerHeight = height - 150 - 60 - 60;
      const maxSize = (innerWidth < innerHeight) ? innerWidth : innerHeight;
      return (maxSize < 400) ? maxSize : 400;
    });
    const cssVars = computed(() => ({
      '--size': `${itemSize.value}px`,
    }));
    const focusKey = ref('');
    const calculatedOffset = computed(() => {
      try {
        const index = items.value.findIndex((i) => i.key === focusKey.value);
        if (index === -1) {
          return 0;
        }
        return index - 1;
      } catch (err) {
        // pass
      }
      return 0;
    });
    const paginate = (offset:number) => {
      if (offset === 0) {
        focusKey.value = '';
      } else {
        const index = calculatedOffset.value + 1 + offset;
        const { key } = items.value[index];
        focusKey.value = key;
      }
    };
    const setFocus = (key:string) => {
      focusKey.value = key;
    };
    const play = () => {
      setTimeout(() => {
        focusKey.value = '';
      }, 1000);
    };
    // eslint-disable-next-line arrow-body-style
    const paginatedItems = computed(() => {
      const numItems = 10;
      return items.value.slice(calculatedOffset.value, calculatedOffset.value + numItems);
    });
    const debug = reactive({
      focusKey,
      calculatedOffset,
      itemSize,
      viewport,
    });
    // live-colors
    watch(current, (item) => {
      if (item.media.releases && item.media.releases.length) {
        const { image } = item.media.releases[0];
        if (image && image.rgb) {
          store.dispatch('ui/setPrimaryColor', image.rgb);
        }
      }
    });
    return {
      items,
      current,
      next,
      past,
      cssVars,
      paginate,
      paginatedItems,
      setFocus,
      play,
      //
      debug,
    };
  },
};
</script>

<template>
  <div class="on-air">
    <StationTime />
    <div
      class="debug-panel"
    >
      <button
        @click="paginate(1)"
      >&lt;</button>
      <button
        @click="paginate(0)"
      >reset</button>
      <button
        @click="paginate(-1)"
      >&gt;</button>
    </div>
    <div
      class="schedule"
      :style="cssVars"
    >
      <ScheduleItem
        v-for="(item, index) in paginatedItems"
        :key="`schedule-item-${(item) ? item.key : index}`"
        :schedule-item="item"
        :has-focus="(index === 1)"
        :is-current="(item === current)"
        :class="`pos-${index}`"
        @play="play"
        @click="setFocus(item.key)"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@mixin item {
  position: absolute;
  width: var(--size);
  height: var(--size);
  transition: transform 500ms, filter 500ms, opacity 500ms;
  // next
  &:nth-child(1) {
    z-index: 20;
    transform: translateX(calc(100vw)) scale(1.2);
    opacity: 0;
    pointer-events: none;
  }
  // current
  &:nth-child(2) {
    z-index: 19;
    transform: translateX(0px) scale(1);
  }
  &:nth-child(3) {
    z-index: 18;
    transform: translateX(-140px) scale(0.9);
    opacity: 0.8;
  }
  &:nth-child(4) {
    z-index: 8;
    transform: translateX(-280px) scale(0.7);
    opacity: 0.6;
  }
  &:nth-child(5) {
    z-index: 7;
    transform: translateX(-400px) scale(0.5);
    opacity: 0.2;
  }
  &:nth-child(6) {
    z-index: 6;
    transform: translateX(-520px) scale(0.2);
    opacity: 0.1;
  }
  &:nth-child(n+6) {
    z-index: 5;
    transform: translateX(-550px) scale(0.1);
    opacity: 0;
  }
  &:nth-child(n+3) {
    filter: grayscale(100%);
  }
  /*
  &.is-current {
    z-index: 10;
    transform: translateX(0px) scale(1);
  }
  */
  &.is-next {
    z-index: 11;
    transform: translateX(600px) scale(3.0);
    opacity: 0.1;
    pointer-events: none;
  }

  &:hover {
    //opacity: 1;
    cursor: pointer;
    filter: grayscale(0%);
  }
}

.schedule {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: var(--size);
  overflow: hidden;

  .schedule-item {
    @include item;
  }
}
.debug-panel {
  position: absolute;
  z-index: 999;
}
</style>
