<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, nextTick, onActivated, onDeactivated, ref, watch } from "vue";
import { useDocumentVisibility, useScroll, useThrottleFn, useWindowSize } from "@vueuse/core";

import { useDevice } from "@/composables/device";
import eventBus from "@/eventBus";
import type { AnnotatedSchedule } from "@/stores/schedule";

import FlowItem from "./FlowItem.vue";
import FlowPlaceholderItem from "./FlowPlaceholderItem.vue";

export default defineComponent({
  components: {
    FlowItem,
    FlowPlaceholderItem,
  },
  props: {
    items: {
      type: Array as PropType<Array<AnnotatedSchedule>>,
      default: () => [],
    },
    itemSize: {
      type: Number,
      default: 0,
    },
  },
  emits: ["onItemFocused"],
  setup(props, { emit }) {
    const panelEl = ref<HTMLElement | null>(null);
    const follow = ref(true);
    const { width: vpWidth, height: vpHeight } = useWindowSize();
    const documentVisible = useDocumentVisibility();
    const { isSafari, isMobile } = useDevice();
    const panelStyle = computed(() => {
      const padding = (vpWidth.value - props.itemSize) / 2;
      return {
        paddingLeft: `${padding}px`,
        paddingRight: `${padding}px`,
      };
    });
    const { x: scrollX, y } = useScroll(panelEl);
    const scrollPanelTo = (pos: number, smooth = true) => {
      if (!panelEl.value) {
        return;
      }
      if (smooth) {
        panelEl.value.scrollTo({
          top: 0,
          left: pos,
          // behavior: "smooth", // NOTE: likely we have to use "auto" on safari
          behavior: isSafari && !isMobile ? "auto" : "smooth",
        });
      } else {
        panelEl.value.scrollLeft = pos;
      }
    };
    watch(
      () => scrollX.value,
      (value) => {
        if (value > -10) {
          follow.value = true;
        } else {
          follow.value = false;
        }
      }
    );
    watch(
      () => vpWidth.value * vpHeight.value,
      () => {
        eventBus.emit("radio:flow", "reset");
      }
    );
    watch(
      () => documentVisible.value,
      (value) => {
        if (value) {
          eventBus.emit("radio:flow", "reset");
        }
      }
    );
    // focus
    const onItemFocused = useThrottleFn((item: AnnotatedSchedule) => {
      emit("onItemFocused", item);
    }, 100);
    // events & controls
    eventBus.on("radio:flow", (event) => {
      if (event === "focusNext") {
        scrollPanelTo(scrollX.value + props.itemSize);
      }
      if (event === "focusPrevious") {
        scrollPanelTo(scrollX.value - props.itemSize);
      }
      if (event === "releaseFocus") {
        scrollPanelTo(0);
      }
      //
      if (event === "itemAdded") {
        nextTick(() => {
          scrollPanelTo(scrollX.value - props.itemSize, false);
          if (follow.value) {
            setTimeout(() => {
              scrollPanelTo(0);
            }, 20);
          }
        });
      }
      //
      if (event === "reset") {
        // NOTE: check browser differences
        nextTick(() => {
          if (follow.value) {
            setTimeout(() => {
              scrollPanelTo(0);
            }, 20);
          }
        });
      }
    });
    const lastScrollX = ref(0);
    onDeactivated(() => {
      lastScrollX.value = scrollX.value;
    });
    onActivated(() => {
      nextTick(() => {
        scrollPanelTo(lastScrollX.value, false);
        eventBus.emit("radio:flow", "reset");
      });
    });
    return {
      panelEl,
      panelStyle,
      scrollX,
      follow,
      y,
      //
      onItemFocused,
    };
  },
});
</script>

<template>
  <div
    class="flow"
    :style="{
      '--item-size': `${itemSize}px`,
    }"
  >
    <div ref="panelEl" v-if="items.length > 1" class="panel" :style="panelStyle" id="scrollPanel">
      <FlowItem
        v-for="(item, index) in items"
        :key="`flow-item-${item ? item.key : index}`"
        :item="item"
        :container-x="scrollX"
        @on-focused="onItemFocused(item)"
      />
      <!--
      <div class="cta">
        <p>
          Looking for music played earlier?
          <br />
          See <a href="#">Program</a>!
        </p>
      </div>
      -->
    </div>
    <transition name="fade">
      <div v-if="items.length < 1" class="placeholder">
        <FlowPlaceholderItem />
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/mixins";

.flow {
  position: relative;
  height: calc(var(--item-size) + 120px);
  width: 100%;

  > .panel {
    @include mixins.hide-scrollbar;

    height: 100%;
    width: 100%;
    overflow-x: scroll;
    overflow-y: hidden;
    display: flex;
    scroll-snap-type: x mandatory;
    direction: rtl;

    .flow-item {
      direction: ltr;
      flex: 0 0 var(--item-size);
      margin: 60px 0;
      display: flex;
      scroll-snap-align: center;
    }

    .cta {
      height: var(--item-size);
      width: var(--item-size);
      direction: ltr;
      flex: 0 0 var(--item-size);
      margin: 60px 100px 60px 0;
      display: flex;
      scroll-snap-align: center;
      align-items: center;
      justify-content: center;
      text-align: center;
    }
  }

  .placeholder {
    top: 0;
    position: absolute;
    height: 100%;
    width: 100%;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 15;
  }
}

// placeholder transitions
.fade-enter-active,
.fade-leave-active {
  transition: opacity 300ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>
