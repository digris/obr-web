<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue";
import { useWindowSize, whenever } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { round } from "lodash-es";

import { usePlayerState } from "@/composables/player";
import eventBus from "@/eventBus";
import type { AnnotatedSchedule } from "@/stores/schedule";
import { useScheduleStore } from "@/stores/schedule";
import { useUiStore } from "@/stores/ui";
import { preloadImage } from "@/utils/image";

import Flow from "./flow/Flow.vue";
import FocusedEmission from "./focused/FocusedEmissionMobile.vue";
import FocusedMedia from "./focused/FocusedMediaMobile.vue";
import Rating from "./rating/Rating.vue";

export default defineComponent({
  components: {
    Flow,
    FocusedEmission,
    FocusedMedia,
    Rating,
  },
  setup() {
    const { isLive } = usePlayerState();
    const { setPrimaryColor } = useUiStore();
    const { items, current: currentItem, next: nextItem } = storeToRefs(useScheduleStore());
    const { width: vpWidth, height: vpHeight } = useWindowSize();
    const itemSize = computed(() => {
      const maxByWidth = round(vpWidth.value * 0.7);
      // NOTE: vpHeight minus menu, time, rating & player
      const maxByHeight = vpHeight.value - 360;
      const max = Math.min(maxByWidth, maxByHeight);
      return Math.max(Math.min(max, 800), 240);
    });
    const debugOffset = ref(0);
    const offset = computed(() => {
      return debugOffset.value;
    });
    const paginatedItems = computed(() => {
      const numItems = 12;
      return items.value.slice(offset.value, offset.value + numItems);
    });
    const focusedItemKey = ref("");
    const onItemFocused = (item: AnnotatedSchedule) => {
      focusedItemKey.value = item.key;
    };
    const focusedItem = computed((): AnnotatedSchedule | null => {
      // NOTE: we use all items here (not paginatedItems)
      const item = items.value.find((i: AnnotatedSchedule) => i.key === focusedItemKey.value);
      return item ? item : null;
    });
    watch(
      () => focusedItem.value,
      (item: AnnotatedSchedule | null) => {
        const rgb = item?.media?.image?.rgb;
        if (rgb) {
          setPrimaryColor(rgb);
        }
      }
    );
    watch(
      () => currentItem.value,
      () => {
        eventBus.emit("radio:flow", "reset");
      }
    );
    whenever(isLive, () => eventBus.emit("radio:flow", "releaseFocus"));
    // NOTE: preload upcoming images
    const nextImage = computed(() => {
      return nextItem.value?.media?.releases?.length
        ? nextItem.value.media.releases[0].image
        : null;
    });
    watch(
      () => nextImage.value,
      (imageObj) => preloadImage(imageObj)
    );
    return {
      itemSize,
      paginatedItems,
      debugOffset,
      onItemFocused,
      focusedItemKey,
      focusedItem,
      nextImage,
    };
  },
});
</script>

<template>
  <div class="radio">
    <div class="emission">
      <FocusedEmission
        v-if="focusedItem?.emission"
        :emission="focusedItem.emission"
        :playlist="focusedItem.playlist"
      />
    </div>
    <div class="flow">
      <Flow :items="paginatedItems" :item-size="itemSize" @on-item-focused="onItemFocused" />
    </div>
    <div class="media">
      <FocusedMedia v-if="focusedItem?.media" :media="focusedItem.media" />
    </div>
    <div class="rating">
      <Rating v-if="focusedItem?.media" :media="focusedItem.media" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.radio {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  margin-bottom: 200px;
  justify-content: flex-start;

  > .emission {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 68px;
    padding: 0 1rem;
    width: 100%;
    text-align: center;

    .focused-emission {
      position: absolute;
      z-index: 15;
      padding: inherit;
    }
  }

  > .flow {
    background: transparent;
    margin: -60px 0;
  }

  > .media {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 68px;
    text-align: center;
    padding: 0 1rem;

    .focused-media {
      position: absolute;
      z-index: 15;
      padding: inherit;
    }
  }

  > .rating {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
