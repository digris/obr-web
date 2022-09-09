<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import type { PropType } from "vue";
import { defineComponent, ref } from "vue";
import { useScroll } from '@vueuse/core';
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
  setup() {
    const el = ref<HTMLElement | null>(null)
    const { x: scrollX, y, isScrolling, arrivedState, directions } = useScroll(el);
    return {
      el,
      scrollX,
      y,
      isScrolling,
      arrivedState,
      directions,
    };
  },
});
</script>

<template>
  <div class="flow">
    <div ref="el" v-if="items.length > 2" class="panel">
      <FlowItem
        v-for="(item, index) in items"
        :key="`flow-item-${item ? item.key : index}`"
        :id="item.key"
        :item="item"
        :container-x="scrollX"
        :style="{
          zIndex: 100 - index,
        }"
      />
    </div>
    <pre v-text="{
      scrollX,
      isScrolling,
      // arrivedState,
      // directions,
    }" />
  </div>
</template>

<style lang="scss" scoped>
.flow {
  width: 100%;
  > .panel {
    text-align: left;
    width: 100%;
    height: 450px;
    overflow-x: scroll;
    display: flex;
    box-sizing: border-box;
    //border: 1px solid #000;
    scroll-snap-type: x mandatory;
    padding: 50px 30%;
    direction: rtl;
    z-index: 90;
    > div {
      direction: ltr;
      flex: 0 0 200px;
      //margin: 0 -60px;
      margin: 60px 0;
      //margin: 60px -60px;
      //margin: 0 10px;
      width: 200px;
      //overflow: hidden;
      //overflow: visible;
      background-color: #663399;
      color: #fff;
      font-size: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      scroll-snap-align: center;
    }
  }
}
</style>
