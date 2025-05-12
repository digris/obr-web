<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue";
import { useWindowSize, whenever } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { round } from "lodash-es";

import Spectrogram from "@/components/audio/Spectrogram.vue";
import { useAnalytics } from "@/composables/analytics";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useSettings } from "@/composables/settings";
import eventBus from "@/eventBus";
import type { AnnotatedSchedule } from "@/stores/schedule";
import { useScheduleStore } from "@/stores/schedule";
import { useTimeStore } from "@/stores/time";
import { useUiStore } from "@/stores/ui";
import { getContrastColor } from "@/utils/color";

import Flow from "./flow/Flow.vue";
import FlowNews from "./flow/FlowNews.vue";
import PaginateButton from "./flow/PaginateButton.vue";
import FocusedEmission from "./focused/FocusedEmission.vue";
import FocusedMedia from "./focused/FocusedMedia.vue";
import RadioHeader from "./RadioHeader.vue";
import Rating from "./rating/Rating.vue";

export default defineComponent({
  components: {
    RadioHeader,
    Flow,
    FlowNews,
    FocusedEmission,
    FocusedMedia,
    PaginateButton,
    Rating,
    Spectrogram,
  },
  setup() {
    const { time } = storeToRefs(useTimeStore());
    const { endPlayNews } = usePlayerControls();
    const { isLive, isNews } = usePlayerState();
    const { setPrimaryColor } = useUiStore();
    const { userSettings } = useSettings();
    const { items, current: currentItem } = storeToRefs(useScheduleStore());
    const { width: vpWidth, height: vpHeight } = useWindowSize();
    const { logUIEvent } = useAnalytics();
    const itemSize = computed(() => {
      const maxByWidth = round(vpWidth.value * 0.7);
      // NOTE: vpHeight minus menu, time, rating & player
      const maxByHeight = vpHeight.value - 380;
      const max = Math.min(maxByWidth, maxByHeight);
      return Math.max(Math.min(max, 800), 240);
    });
    const debugOffset = ref(0);
    const offset = computed(() => {
      return debugOffset.value;
    });
    const paginatedItems = computed(() => {
      const numItems = 8;
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
    const hasNext = computed(() => {
      if (!focusedItem.value) {
        return false;
      }
      const index = items.value.findIndex((i: AnnotatedSchedule) => i.key === focusedItemKey.value);
      return index > 0;
    });
    const hasPrevious = computed(() => {
      if (!focusedItem.value) {
        return false;
      }
      // if (isNews.value) {
      //   return false;
      // }
      const index = paginatedItems.value.findIndex(
        (i: AnnotatedSchedule) => i.key === focusedItemKey.value
      );
      return index < paginatedItems.value.length - 1;
    });
    const focusNext = () => {
      eventBus.emit("radio:flow", "focusNext");
      logUIEvent("cover-flow:next");
    };
    const focusPrevious = () => {
      eventBus.emit("radio:flow", "focusPrevious");
      logUIEvent("cover-flow:previous");
    };
    const releaseFocus = () => {
      eventBus.emit("radio:flow", "releaseFocus");
      logUIEvent("cover-flow:reset");
    };
    whenever(isLive, () => eventBus.emit("radio:flow", "releaseFocus"));

    // visualisation
    const spectrogramVisible = computed(() => userSettings.value?.testingEnabled);
    const { primaryColor } = storeToRefs(useUiStore());
    const spectrogramColor = computed(() => {
      const fg = getContrastColor(primaryColor.value);
      return `rgb(${fg.join(" ")} / 10%)`;
    });
    return {
      time,
      itemSize,
      paginatedItems,
      debugOffset,
      onItemFocused,
      focusedItemKey,
      focusedItem,
      //
      endPlayNews,
      isNews,
      //
      hasNext,
      hasPrevious,
      focusNext,
      focusPrevious,
      releaseFocus,
      // visualisation
      primaryColor,
      spectrogramVisible,
      spectrogramColor,
      vpWidth,
    };
  },
});
</script>

<template>
  <div
    class="radio"
    :style="{
      '--item-size': `${itemSize}px`,
    }"
    :class="{
      'is-news': isNews,
    }"
  >
    <div class="header-container">
      <RadioHeader :item="focusedItem" @release-focus="releaseFocus" />
    </div>
    <div class="main">
      <div class="left">
        <FocusedEmission
          v-if="focusedItem?.emission"
          :emission="focusedItem.emission"
          :playlist="focusedItem.playlist"
        />
        <div class="paginate">
          <PaginateButton :disabled="!hasPrevious" :rotate="180" @click="focusPrevious" />
        </div>
      </div>
      <div class="flow">
        <Flow
          v-show="true"
          :items="paginatedItems"
          :item-size="itemSize"
          @on-item-focused="onItemFocused"
          :style="{
            opacity: isNews ? 0.125 : 1,
          }"
        />
        <transition name="news">
          <FlowNews v-show="isNews" :item-size="itemSize" />
        </transition>
      </div>
      <div class="right">
        <FocusedMedia v-if="focusedItem?.media" :media="focusedItem.media" />
        <div class="paginate">
          <PaginateButton :disabled="!hasNext" @click="focusNext" />
        </div>
        <div v-if="isNews" @click="endPlayNews" class="skip-news">
          <div class="skip-news__label">Skip News</div>
          <PaginateButton />
        </div>
      </div>
    </div>
    <div class="rating">
      <Rating v-if="focusedItem?.media" :media="focusedItem.media" />
    </div>
  </div>
  <Spectrogram v-if="spectrogramVisible" :height="200" :width="vpWidth" :color="spectrogramColor" />
</template>

<style lang="scss" scoped>
.radio {
  position: relative;

  > .header-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 124px;
    z-index: 10;

    > .radio-header {
      position: absolute;
      width: var(--item-size);
    }
  }

  > .main {
    display: flex;
    position: relative;

    > .flow {
      overflow: hidden;
      top: 0;
      width: 100%;
      margin: -60px 0;
    }

    > .flow-news {
      overflow: hidden;
      top: 0;
      width: 100%;
      margin: -60px 0;
    }

    > .left,
    > .right {
      top: 0;
      position: absolute;
      height: 100%;
      width: 25%;
      display: flex;
      justify-content: center;
      z-index: 19;

      .metadata {
        width: 100%;
      }

      .paginate {
        top: calc(var(--item-size) / 2 - 60px);
        position: absolute;
        height: 120px;
        width: 120px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 18;
      }
    }

    > .left {
      padding-left: 1rem;
    }

    > .right {
      right: 0;
      padding-right: 1rem;

      .skip-news {
        top: calc(var(--item-size) / 2 - 60px);
        position: absolute;
        height: 120px;
        width: 120px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 18;

        &__label {
          position: absolute;
          height: 120px;
          right: 120px;
          white-space: nowrap;
          padding-right: 1rem;
          display: flex;
          align-items: center;
        }
      }
    }
  }

  > .rating {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 124px;
  }

  &.is-news {
    > .main {
      > .left,
      > .right {
        cursor: wait;

        .metadata {
          opacity: 0.5;
          pointer-events: none;
        }
      }

      > .left {
        .paginate {
          display: none;
        }
      }

      > .right {
        .paginate {
          display: none;
        }
      }
    }

    > .rating {
      opacity: 0.5;
      pointer-events: none;
      cursor: wait;
    }
  }
}

.spectrogram-container {
  position: fixed;
  bottom: 72px;
}

// news panel transition
.news-enter-active,
.news-leave-active {
  transition: opacity 200ms;
}

.news-enter-from {
  opacity: 0;
}

.news-leave-to {
  opacity: 0;
}
</style>
