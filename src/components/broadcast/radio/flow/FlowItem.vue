<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import type { PropType } from "vue";
import { defineComponent, ref, watch, computed, onMounted, nextTick } from "vue";
import { useWindowSize, useThrottleFn, useElementBounding } from "@vueuse/core";
import { round } from "lodash-es";
import { DateTime } from "luxon";
import eventBus from "@/eventBus";
import LazyImage from "@/components/ui/LazyImage.vue";
import PlayButton from "../../onair/button/Play.vue";

export default defineComponent({
  components: {
    LazyImage,
    PlayButton,
  },
  props: {
    item: {
      type: Object as PropType<AnnotatedSchedule>,
      required: true,
    },
    hasFocus: {
      type: Boolean,
      default: false,
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

    const isVisible = computed(() => {
      return relativePosition.value > -4;
    });

    const image = computed(() => {
      if (!props.item.media.releases) {
        return null;
      }
      return props.item.media.releases[0].image;
    });

    const cssVars = computed(() => {
      // const rbg = props.item.r
      const rgb = image.value?.rgb ?? [0, 0, 0];
      return {
        "--c-bg": rgb.join(","),
      };
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
    });

    // handle item focus
    const throttledOnFocused = useThrottleFn(() => {
      emit("onFocused");
    }, 50);
    watch(
      () => relativePosition.value,
      (value) => {
        if (value > -0.3 && value < 0.3) {
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
        return round(width.value * n - width.value * n * 0.1, 3);
      } else {
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
    return {
      el,
      // offset,
      elX,
      offset,
      focus,
      relativePosition,
      isVisible,
      cssVars,
      image,
      // x,
      // right,
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
      ...cssVars,
      opacity: scale,
    }"
  >
    <div v-if="false" class="container">
      <pre v-text="{ offset, focus, relativePosition, translateX, scale, timeStart, cssVars }" />
    </div>
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
        <div class="actions">
          <PlayButton />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/*
variables defined in parent component(s):
 --item-size
*/
.flow-item {
  //background-color: rgba(255, 255, 255, 0.2);
  width: var(--item-size);
  height: var(--item-size);
  flex-direction: column;
  font-size: 12px;
  position: relative;
  //z-index: 99;
  .translate-x {
    position: absolute;
    top: 0;
    left: 0;
    width: var(--item-size);
    height: var(--item-size);
    //background: deepskyblue;
    //border: 1px solid deepskyblue;
    pointer-events: none;
  }
  .scale {
    position: absolute;
    top: 0;
    left: 0;
    width: var(--item-size);
    height: var(--item-size);
    //border: 1px solid black;
    background: rgba(var(--c-bg, 0.9));
    transform-origin: left;
  }
  .actions {
    position: absolute;
    z-index: 999;
    top: 0;
    left: 0;
    .circle-button {
      background: rgba(var(--c-bg), 1);
      &:hover {
        background: rgba(var(--c-bg), 0.8);
      }
    }
  }
  &:hover {
    background: #6def6d;
  }
}
</style>
