<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import type { PropType } from "vue";
import { defineComponent, ref, watch, computed } from 'vue';
import { useWindowSize } from '@vueuse/core'
import { round } from "lodash-es";
import {DateTime} from 'luxon';

export default defineComponent({
  props: {
    item: {
      type: Object as PropType<AnnotatedSchedule>,
      required: true,
    },
    containerX: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    const el = ref<HTMLElement | null>(null);
    const elX = ref(0);
    const { width: vpWidth } = useWindowSize();

    const offset = computed(() => {
      return round(elX.value - vpWidth.value / 2, 1);
    });

    const focus = computed(() => {
      const rawFocus = 1 - (offset.value * -1) / vpWidth.value;
      const roundedFocus = round(rawFocus, 3);
      return Math.max(Math.min(roundedFocus, 2), 0);
    });

    const timeEnd = computed(() => {
      return props.item.dtEnd.toLocaleString(DateTime.TIME_24_WITH_SECONDS);
    });

    // const offset = computed(() => {
    //   if (!el.value) {
    //     return 0;
    //   }
    //   const { left, width } = el.value.getBoundingClientRect();
    //   const elX = left + width / 2;
    //   console.debug('BB', left, props.containerX);
    //   return elX;
    //   return props.containerX;
    // });
    watch(
      () => props.containerX,
      () => {
        if (!el.value) {
          return;
        }
        const { left, width } = el.value.getBoundingClientRect();
        elX.value = round(left + width / 2, 1);
      }
    );

    return {
      el,
      // offset,
      elX,
      offset,
      focus,
      // x,
      // right,
      timeEnd,
    };
  },
});
</script>

<template>
  <div
    ref="el"
    v-if="item"
    class="flow-item"
    :style="{
      opacity: focus,
    }"
  >
    <small>{{ item.media.name }}</small>
    <!--
    <pre v-text="{elX, offset, focus}" />
    -->
    <!--
    <small v-text="focus" />
    -->
    <small v-text="timeEnd" />
    <div
      class="pt"
      :style="{
        transform: `scale(${focus})`,
      }"
    />
  </div>
</template>


<style lang="scss" scoped>
.flow-item {
  width: 200px;
  height: 200px;
  //border: 2px solid red;
  //overflow: hidden;
  //overflow: visible;
  flex-direction: column;
  font-size: 50%;
  position: relative;
  z-index: 99;
  > pre,
  > small {
    font-size: 50%;
  }
  > .pt {
    width: 200px;
    height: 200px;
    background: rgba(200, 0, 200, 0.25);
    position: absolute;
    border: 4px solid #6def6d;
    z-index: 101;
  }
}
</style>
