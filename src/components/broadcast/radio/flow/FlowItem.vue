<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, nextTick, onMounted, ref, watch } from "vue";
import { useElementBounding, useThrottleFn, useWindowSize } from "@vueuse/core";
import { DateTime } from "luxon";
import { round } from "lodash-es";

import LazyImage from "@/components/ui/LazyImage.vue";
import eventBus from "@/eventBus";
import type { AnnotatedSchedule } from "@/stores/schedule";
import { getContrastColor } from "@/utils/color";

import FlowItemPlay from "./FlowItemPlay.vue";
import Ticker from "./ticker/Ticker.vue";

const BASE_Z_INDEX = 12;

export default defineComponent({
  components: {
    LazyImage,
    FlowItemPlay,
    Ticker,
  },
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
  emits: ["onFocused"],
  setup(props, { emit }) {
    const el = ref<HTMLElement | null>(null);
    const elX = ref(0);
    const { width: vpWidth } = useWindowSize();
    const { width } = useElementBounding(el);

    const offset = computed(() => {
      return round(elX.value - vpWidth.value / 2, 2);
    });

    const focus = computed(() => {
      const rawFocus = 1 - (offset.value * -1) / vpWidth.value;
      const roundedFocus = round(rawFocus, 3);
      return Math.max(Math.min(roundedFocus, 2), 0);
    });

    const timeStart = computed(() => {
      return props.item.dtStart.toLocaleString(DateTime.TIME_24_WITH_SECONDS);
    });

    const relativePosition = computed(() => {
      return round(offset.value / width.value, 3);
    });

    const hasFocus = computed(() => {
      return relativePosition.value > -0.7 && relativePosition.value < 0.3;
    });

    const isVisible = computed(() => {
      return relativePosition.value > -4;
    });

    const media = computed(() => {
      return props.item.media;
    });

    const release = computed(() => {
      if (!media.value.releases) {
        return null;
      }
      return media.value.releases[0];
    });

    const image = computed(() => {
      return release.value?.image ?? null;
    });
    const updateElPosition = () => {
      if (!el.value) {
        return;
      }
      const { left: elLeft, width: elWidth } = el.value.getBoundingClientRect();
      elX.value = round(elLeft + elWidth / 2, 1);
    };
    onMounted(updateElPosition);
    watch(() => props.containerX, updateElPosition);
    eventBus.on("radio:flow", (event) => {
      if (event === "itemAdded") {
        nextTick(updateElPosition);
      }
      if (event === "reset") {
        nextTick(updateElPosition);
      }
    });

    // handle item focus
    const throttledOnFocused = useThrottleFn(() => {
      emit("onFocused");
    }, 50);
    watch(
      () => relativePosition.value,
      (value) => {
        if (value > -0.7 && value < 0.3) {
          throttledOnFocused();
        }
      }
    );

    // transforms
    const translateX = computed(() => {
      if (relativePosition.value > 0) {
        return round((relativePosition.value * vpWidth.value) / 2, 3);
      }
      const n = Math.abs(relativePosition.value);
      if (vpWidth.value > 1024) {
        // stacked layout
        return round(width.value * n - width.value * n * 0.1, 3);
      } else {
        // coverflow layout
        return round(width.value * n * 0.125, 3);
      }
    });
    const scale = computed(() => {
      if (relativePosition.value > 0) {
        const rawScale = relativePosition.value * 1.1 + 1;
        return Math.min(round(rawScale, 3), 1.2);
      }
      const n = Math.abs(relativePosition.value);
      const rawScale = 1 - n * 0.25;
      return Math.max(round(rawScale, 3), 0.2);
    });
    const opacity = computed(() => {
      if (relativePosition.value > 0) {
        const n = relativePosition.value;
        return Math.max(round(1 - n * 2, 3), 0);
      }
      const n = Math.abs(relativePosition.value);
      return Math.max(round(1 - n / 3, 3), 0);
    });
    const style = computed(() => {
      return {
        zIndex: BASE_Z_INDEX + round(relativePosition.value),
        opacity: opacity.value,
        // NOTE: grayscale filter has performance issues on iOS
        // filter: `grayscale(${1 - opacity.value})`,
        // filter: `grayscale(${grayscale.value})` ,
      };
    });
    const cssVars = computed(() => {
      const bg = image.value?.rgb ?? [0, 0, 0];
      const fg = getContrastColor(bg);
      return {
        "--c-bg": bg.join(" "),
        "--c-fg": fg.join(" "),
      };
    });

    return {
      el,
      elX,
      offset,
      focus,
      relativePosition,
      hasFocus,
      isVisible,
      style,
      cssVars,
      image,
      release,
      timeStart,
      translateX,
      scale,
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
      ...style,
      ...cssVars,
    }"
  >
    <div
      v-if="isVisible"
      class="translate-x"
      :style="{
        transform: `translateX(${translateX}px)`,
      }"
    >
      <div
        class="scale"
        :style="{
          transform: `scale(${scale})`,
        }"
      >
        <LazyImage :image="image" />
        <transition name="fade">
          <div v-if="hasFocus" class="actions">
            <FlowItemPlay :item="item" />
          </div>
        </transition>
        <Ticker v-if="release?.isNew" text="New Release" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/*
variables defined in parent component(s):
 --item-size
*/
@use "@/style/base/typo";
@use "@/style/base/responsive";

.flow-item {
  position: relative;
  height: var(--item-size);
  width: var(--item-size);
  display: none;
  flex-direction: column;
  font-size: 12px;

  .translate-x {
    top: 0;
    position: absolute;
    height: var(--item-size);
    width: var(--item-size);
    left: 0;
  }

  .scale {
    top: 0;
    position: absolute;
    height: var(--item-size);
    width: var(--item-size);
    left: 0;
    background: rgb(var(--c-bg) / 90%);
    transform-origin: left;
    box-shadow: 0 0 20px rgb(0 0 0 / 50%);
  }

  .actions {
    top: 0;
    position: absolute;
    height: 100%;
    width: 100%;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;

    .circle-button {
      background: rgb(var(--c-bg) / 100%);

      &:hover {
        background: rgb(var(--c-bg) / 80%);
      }
    }
  }

  .ticker {
    @include typo.large;

    top: 20px;
    position: absolute;
    width: 100%;
    left: 0;

    @include responsive.bp-medium {
      top: 10px;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>
