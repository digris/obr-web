<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import type { PropType } from "vue";
import { defineComponent, ref, computed, nextTick, watch, onActivated, onDeactivated } from "vue";
import { useScroll, useThrottleFn, useWindowSize, useDocumentVisibility } from "@vueuse/core";
import eventBus from "@/eventBus";
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
    const isDocumentVisible = useDocumentVisibility();
    const panelStyle = computed(() => {
      const padding = (vpWidth.value - props.itemSize) / 2;
      return {
        paddingLeft: `${padding}px`,
        paddingRight: `${padding}px`,
      };
    });
    const { x: scrollX, y, isScrolling, arrivedState, directions } = useScroll(panelEl);
    const scrollPanelTo = (pos: number, smooth = true) => {
      if (!panelEl.value) {
        return;
      }
      if (smooth) {
        panelEl.value.scrollTo({
          top: 0,
          left: pos,
          behavior: "smooth", // NOTE: likely we have to use "auto" on safari
        });
      } else {
        panelEl.value.scrollLeft = pos;
      }
    };
    watch(
      () => scrollX.value,
      (value) => {
        if (value > -0.5) {
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
      () => isDocumentVisible.value,
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
      isScrolling,
      arrivedState,
      directions,
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
      <!---->
      <div class="cta">
        <p>
          Looking for music played earlier?
          <br />
          See <a href="#">Program</a>!
        </p>
      </div>
    </div>
    <transition name="fade">
      <div v-if="items.length < 1" class="placeholder">
        <FlowPlaceholderItem />
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
.flow {
  width: 100%;
  height: calc(var(--item-size) + 120px);
  position: relative;
  > .panel {
    width: 100%;
    height: 100%;
    overflow-x: scroll;
    overflow-y: hidden;
    display: flex;
    scroll-snap-type: x mandatory;
    //padding: 0 30%;
    direction: rtl;
    //scroll-behavior: smooth;
    /**/
    &::-webkit-scrollbar {
      display: none;
    }
    .flow-item {
      /* flow */
      direction: ltr;
      flex: 0 0 var(--item-size);
      margin: 60px 0;
      display: flex;
      scroll-snap-align: center;
    }
    /**/
    .cta {
      direction: ltr;
      flex: 0 0 var(--item-size);
      margin: 60px 100px 60px 0;
      display: flex;
      scroll-snap-align: center;
      width: var(--item-size);
      height: var(--item-size);
      //background: black;
      align-items: center;
      justify-content: center;
      text-align: center;
    }
  }
  .placeholder {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20;
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
