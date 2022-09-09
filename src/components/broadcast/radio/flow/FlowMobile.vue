<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import type { PropType } from "vue";
import { defineComponent, ref, computed, nextTick, watch } from 'vue';
import { useScroll, useWindowSize } from "@vueuse/core";
import { round } from "lodash-es";
import eventBus from "@/eventBus";
import FlowItem from "./FlowItem.vue";

export default defineComponent({
  components: {
    FlowItem,
  },
  props: {
    items: {
      type: Array as PropType<Array<AnnotatedSchedule>>,
      default: () => [],
    },
  },
  emits: ["on-item-focused"],
  setup() {
    const panelEl = ref<HTMLElement | null>(null);
    const follow = ref(true);
    const { width: vpWidth } = useWindowSize();
    const itemSize = computed(() => {
      // return 273; // mobile
      // return 400; // large
      const size = round(vpWidth.value * 0.7);
      return Math.min(size, 800 );
    });
    const panelStyle = computed(() => {
      const padding = (vpWidth.value - itemSize.value) / 2;
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
          behavior: "smooth",
        });
      } else {
        panelEl.value.scrollLeft = pos;
      }
    };
    watch(
      () => scrollX.value,
      (value) => {
        if (value > -0.2) {
          console.debug('set follow: on');
          follow.value = true;
        } else {
          console.debug('set follow: off');
          follow.value = false;
        }
      }
    );
    // events & controls
    eventBus.on("radio:flow", (event) => {
      if (event === "focusNext") {
        scrollPanelTo(scrollX.value + itemSize.value);
      }
      if (event === "focusPrevious") {
        scrollPanelTo(scrollX.value - itemSize.value);
      }
      if (event === "releaseFocus") {
        scrollPanelTo(0);
      }
      //
      if (event === "itemAdded") {
        nextTick(() => {
          scrollPanelTo(scrollX.value - itemSize.value, false);
          if (follow.value) {
            setTimeout(() => {
              scrollPanelTo(0);
            }, 20);
          }
        });
      }
    });
    return {
      panelEl,
      panelStyle,
      scrollX,
      follow,
      itemSize,
      y,
      isScrolling,
      arrivedState,
      directions,
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
    <div ref="panelEl" v-if="items.length > 1" class="panel" :style="panelStyle">
      <FlowItem
        v-for="(item, index) in items"
        :key="`flow-item-${item ? item.key : index}`"
        :id="item.key"
        :item="item"
        :container-x="scrollX"
        :style="{
          zIndex: 100 - index,
        }"
        @on-focused="$emit('on-item-focused', item)"
      />
      <!--
      <div class="cta">
        <p>Looking for music played earlier?
          <br>
          See <a href="#">Program</a>!</p>
      </div>
      -->
    </div>
    <pre
      v-text="{
        follow,
      }"
    />
  </div>
</template>

<style lang="scss" scoped>
.flow {
  width: 100%;
  //height: calc(var(--item-size) + 160px);
  > .panel {
    width: 100%;
    height: 100%;
    overflow-x: scroll;
    overflow-y: hidden;
    display: flex;
    scroll-snap-type: x mandatory;
    //padding: 0 30%;
    direction: rtl;
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
    /*
    .cta {
      direction: ltr;
      flex: 0 0 auto;
      margin: 60px 0;
      display: flex;
      scroll-snap-align: center;
      width: 100vw;
      max-width: 500px;
      height: var(--item-size);
      //background: black;
      align-items: center;
      justify-content: center;
      text-align: center;
    }
    */
  }
}
</style>
