<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import { ref, computed, defineComponent, watch } from "vue";
import { useWindowSize } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { useTimeStore } from "@/stores/time";
import { useScheduleStore } from "@/stores/schedule";
import { useUiStore } from "@/stores/ui";
import { round } from "lodash-es";
import eventBus from "@/eventBus";
import RadioHeader from "./RadioHeader.vue";
import Flow from "./flow/FlowMobile.vue";
import FocusedEmission from "./focused/FocusedEmission.vue";
import FocusedMedia from "./focused/FocusedMedia.vue";
import PaginateButton from "./flow/PaginateButton.vue";
import Rating from "./rating/Rating.vue";

export default defineComponent({
  components: {
    RadioHeader,
    Flow,
    FocusedEmission,
    FocusedMedia,
    PaginateButton,
    Rating,
  },
  setup() {
    const { time } = storeToRefs(useTimeStore());
    const { setPrimaryColor } = useUiStore();
    const { items, current: currentItem } = storeToRefs(useScheduleStore());
    const { width: vpWidth, height: vpHeight } = useWindowSize();
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
      const index = paginatedItems.value.findIndex(
        (i: AnnotatedSchedule) => i.key === focusedItemKey.value
      );
      return index < paginatedItems.value.length - 1;
    });
    const focusNext = () => {
      eventBus.emit("radio:flow", "focusNext");
    };
    const focusPrevious = () => {
      eventBus.emit("radio:flow", "focusPrevious");
    };
    const releaseFocus = () => {
      eventBus.emit("radio:flow", "releaseFocus");
    };
    return {
      time,
      itemSize,
      paginatedItems,
      debugOffset,
      onItemFocused,
      focusedItemKey,
      focusedItem,
      //
      hasNext,
      hasPrevious,
      focusNext,
      focusPrevious,
      releaseFocus,
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
        <Flow :items="paginatedItems" :item-size="itemSize" @on-item-focused="onItemFocused" />
      </div>
      <div class="right">
        <FocusedMedia v-if="focusedItem?.media" :media="focusedItem.media" />
        <div class="paginate">
          <PaginateButton :disabled="!hasNext" @click="focusNext" />
        </div>
      </div>
    </div>
    <div class="rating">
      <Rating v-if="focusedItem?.media" :media="focusedItem.media" />
    </div>
    <!--
    <div class="emission">
      <FocusedEmission
        v-if="focusedItem?.emission"
        :emission="focusedItem.emission"
        :playlist="focusedItem.playlist"
      />
    </div>
    <div class="flow">
      <Flow :items="paginatedItems" @on-item-focused="onItemFocused" />
    </div>
    <div class="media">
      <FocusedMedia v-if="focusedItem?.media" :media="focusedItem.media" />
    </div>
    <div class="rating">
      <Rating v-if="focusedItem?.media" :media="focusedItem.media" />
    </div>
    <div v-if="false">
      <button @click.prevent="focusPrevious" v-text="`PREV`" />
      <button @click.prevent="focusNext" v-text="`NEXT`" />
      <button @click.prevent="releaseFocus" v-text="`FOLLOW`" />
    </div>
    -->
  </div>
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
    //cursor: pointer;
    z-index: 10;
    > .radio-header {
      position: absolute;
      width: var(--item-size);
    }
  }
  > .main {
    //background: yellow;
    display: flex;
    position: relative;
    > .flow {
      overflow: hidden;
      top: 0;
      width: 100%;
      margin: -60px 0;
    }
    > .left,
    > .right {
      //background: rgba(255, 255, 0, 0.25);
      position: absolute;
      top: 0;
      display: flex;
      justify-content: center;
      height: 100%;
      width: 25%;
      z-index: 24;
      //background: rgba(255, 255, 0, 0.25);
      .metadata {
        width: 100%;
      }
      .paginate {
        position: absolute;
        //height: 100%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 20;
        //z-index: 25;
        height: 120px;
        width: 120px;
        top: calc(var(--item-size) / 2 - 60px);
      }
    }
    > .left {
      padding-left: 1rem;
    }
    > .right {
      right: 0;
      padding-right: 1rem;
    }
  }
  > .rating {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 124px;
  }
}
</style>
