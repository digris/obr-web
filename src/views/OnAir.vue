<script lang="ts">
import {
  computed,
  ref,
  watch,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

import StationTime from '@/components/broadcast/onair/station-time/StationTime.vue';
import Schedule from '@/components/broadcast/onair/Schedule.vue';
import FocusedEmission from '@/components/broadcast/onair/FocusedEmission.vue';
import FocusedMedia from '@/components/broadcast/onair/FocusedMedia.vue';
import PaginateButton from '@/components/broadcast/onair/button/PaginateNext.vue';

export default defineComponent({
  components: {
    StationTime,
    Schedule,
    FocusedEmission,
    FocusedMedia,
    PaginateButton,
  },
  setup() {
    const route = useRoute();
    const store = useStore();
    const viewport = computed(() => store.getters['ui/viewport']);
    const current = computed(() => store.getters['schedule/current']);
    const next = computed(() => store.getters['schedule/next']);
    const past = computed(() => store.getters['schedule/past']);
    const items = computed(() => [next.value || null, current.value || null, ...past.value]);
    const itemSize = computed(() => {
      const { width } = viewport.value;
      // console.debug('width, height', width, height);
      // const innerWidth = width - 60 * 2;
      // const innerHeight = height - 150 - 60 - 60;
      // const maxSize = (innerWidth < innerHeight) ? innerWidth : innerHeight;
      // const maxSize = width * 0.3;
      const maxSize = width * 0.4;
      return (maxSize < 720) ? maxSize : 720;
    });
    const cssVars = computed(() => ({
      '--size': `${itemSize.value}px`,
      '--item-size': `${itemSize.value}px`,
      '--item-offset': `${itemSize.value * 0.12}px`,
      // '--item-size': '600px',
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
    const focused = computed(() => {
      // TODO: check implementation
      try {
        return items.value[calculatedOffset.value + 1];
      } catch {
        return null;
      }
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
    // eslint-disable-next-line arrow-body-style
    const paginatedItems = computed(() => {
      const numItems = 10;
      return items.value.slice(calculatedOffset.value, calculatedOffset.value + numItems);
    });
    const hasPrevious = computed(() => {
      return items.value[calculatedOffset.value + 2] !== undefined;
      // console.debug(calculatedOffset.value);
      // console.table(items.value);
      // return false;
    });
    const hasNext = computed(() => {
      return items.value[calculatedOffset.value - 1] !== undefined;
      // console.debug(calculatedOffset.value);
      // console.table(items.value);
      // return false;
    });
    // live-colors
    // watch(current, (item) => {
    //   if (item.media.releases && item.media.releases.length) {
    //     const { image } = item.media.releases[0];
    //     if (image && image.rgb) {
    //       store.dispatch('ui/setPrimaryColor', image.rgb);
    //     }
    //   }
    // });
    watch(
      () => route.name,
      async (newName) => {
        if (newName !== 'home') {
          return;
        }
        const item = focused.value;
        if (item && item.media.releases && item.media.releases.length) {
          const { image } = item.media.releases[0];
          if (image && image.rgb) {
            store.dispatch('ui/setPrimaryColor', image.rgb);
          }
        }
      },
    );
    watch(focused, (item) => {
      if (route.name !== 'home') {
        return;
      }
      if (item.media.releases && item.media.releases.length) {
        const { image } = item.media.releases[0];
        if (image && image.rgb) {
          store.dispatch('ui/setPrimaryColor', image.rgb);
        }
      }
    });
    return {
      items,
      itemSize,
      current,
      focused,
      next,
      past,
      cssVars,
      paginate,
      paginatedItems,
      hasPrevious,
      hasNext,
      setFocus,
    };
  },
});
</script>

<template>
  <div
    class="on-air"
    :style="cssVars"
  >
    <StationTime
      @release-focus="setFocus('')"
    />
    <div
      class="left"
    >
      <FocusedEmission
        v-if="focused && focused.emission && focused.playlist"
        :emission="focused.emission"
        :playlist="focused.playlist"
      />
      <PaginateButton
        :disabled="(!hasPrevious)"
        :rotate="180"
        @click="paginate(1)"
      />
    </div>
    <div
      class="center"
    >
      <div
        class="placeholder"
      />
    </div>
    <div
      class="right"
    >
      <FocusedMedia
        v-if="focused && focused.media"
        :media="focused.media"
      />
      <PaginateButton
        :disabled="(!hasNext)"
        @click="paginate(-1)"
      />
    </div>
    <div
      class="actions"
    >
      (( ACTIONS ))
    </div>
    <Schedule
      :current="current"
      :items="paginatedItems"
      :item-size="itemSize"
      @on-focus="setFocus"
    />
  </div>
</template>

<style lang="scss" scoped>
.on-air {
  position: relative;
  display: grid;
  grid-row-gap: 0.25rem;
  grid-column-gap: 1rem;
  grid-template-areas:
    ". station-time ."
    "left center right"
    ". actions .";
  grid-template-columns: auto var(--item-size) auto;
  .station-time {
    grid-area: station-time;
  }
  .left {
    grid-area: left;
    padding: 1rem;
  }
  .center {
    grid-area: center;
    .placeholder {
      width: var(--item-size);
      height: calc(var(--item-size) + 40px);
    }
  }
  .right {
    grid-area: right;
    padding: 1rem;
  }
  .actions {
    display: flex;
    grid-area: actions;
    align-items: center;
    justify-content: center;
  }
  .left,
  .right {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    .metadata {
      position: absolute;
      top: 12px;
      left: 2rem;
    }
  }
}
</style>
