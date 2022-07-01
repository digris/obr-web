<script lang="ts">
import { computed, defineComponent } from "vue";

import ScheduleItem from "@/components/broadcast/onair/ScheduleItem.vue";

export default defineComponent({
  components: {
    ScheduleItem,
  },
  props: {
    items: {
      type: Array,
      default: () => [],
    },
    current: {
      type: Object,
      default: () => {},
    },
    itemSize: {
      type: Number,
      default: 0,
    },
  },
  emits: ["onFocus"],
  setup(props, { emit }) {
    const cssVars = computed(() => ({
      "--item-size": `${props.itemSize}px`,
      "--item-offset": `${props.itemSize * 0.12}px`,
    }));
    const setFocus = (key: string) => {
      emit("onFocus", key);
    };
    const play = () => {
      // TODO: not needed without time-shift
      setTimeout(() => {
        emit("onFocus", "");
      }, 2000);
    };
    return {
      cssVars,
      setFocus,
      play,
    };
  },
});
</script>

<template>
  <div class="schedule" :style="cssVars">
    <ScheduleItem
      v-for="(item, index) in items"
      :key="`schedule-item-${item ? item.key : index}`"
      :schedule-item="item"
      :position="index"
      :has-focus="index === 1"
      :is-current="item === current"
      :class="`pos-${index}`"
      @play="play"
      @click="setFocus(item.key)"
    />
  </div>
</template>
<style lang="scss" scoped>
//@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@mixin item {
  position: absolute;
  width: var(--item-size);
  height: var(--item-size);
  box-shadow: 0 0 20px rgb(0 0 0 / 50%);
  transform-origin: left;
  transition: transform 500ms, filter 500ms, opacity 500ms;
  pointer-events: none;
  // next
  &:nth-child(1) {
    z-index: 20;
    transform: translateX(calc(100vw)) scale(1.2);
    opacity: 0;
  }
  // current
  &:nth-child(2) {
    z-index: 19;
    transform: translateX(0px) scale(1);
    pointer-events: auto;
  }
  &:nth-child(3) {
    z-index: 18;
    transform: translateX(calc(var(--item-offset) * -1)) scale(0.8);
    opacity: 0.8;
    pointer-events: auto;
  }
  &:nth-child(4) {
    z-index: 8;
    transform: translateX(calc(var(--item-offset) * -2)) scale(0.6);
    opacity: 0.6;
    pointer-events: auto;
  }
  &:nth-child(5) {
    z-index: 7;
    transform: translateX(calc(var(--item-offset) * -3)) scale(0.4);
    opacity: 0;
  }
  &:nth-child(n + 6) {
    z-index: 6;
    transform: translateX(calc(var(--item-offset) * -4)) scale(0.2);
    opacity: 0;
  }
  &:nth-child(n + 3) {
    filter: grayscale(100%);
  }
  &.is-next {
    z-index: 11;
    transform: translateX(600px) scale(3);
    opacity: 0.1;
    pointer-events: none;
  }
  &:hover {
    cursor: pointer;
    filter: grayscale(0%);
  }
}

.schedule {
  position: absolute;
  top: 114px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: calc(var(--item-size) + 40px);
  overflow: hidden;
  pointer-events: none;
  .schedule-item {
    @include item;
  }
  //TODO: just a quick fix..
  @include responsive.bp-small {
    .schedule-item {
      &:not(:nth-child(2)) {
        display: none;
      }
    }
  }
}
</style>
