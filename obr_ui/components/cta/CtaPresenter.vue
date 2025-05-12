<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import { onClickOutside, useElementBounding, useElementSize, useWindowSize } from "@vueuse/core";

const isVisible = ref(false);

const el = ref<HTMLElement | null>(null);
const targetEl = ref<HTMLElement | null>(null);

onClickOutside(el, () => {
  console.debug("clicked outside");
  isVisible.value = false;
});

const {
  // width: vpWidth,
  height: vpHeight,
} = useWindowSize();

const { width, height } = useElementSize(el);

const pos = computed(() => {
  return {
    // x: Math.round((vpWidth.value - width.value) / 2),
    x: targetPos.value?.x - width.value + 2 ?? 0,
    y: Math.round((vpHeight.value - height.value) / 2),
  };
});

const {
  x: targetX,
  y: targetY,
  width: targetWidth,
  // height: targetHeight,
} = useElementBounding(targetEl);

const targetPos = computed(() => {
  return {
    x: Math.round(targetX.value + targetWidth.value / 2),
    y: Math.round(targetY.value - 4),
  };
});

const linePos = computed(() => {
  return {
    x1: pos.value.x + width.value ?? 0,
    y1: pos.value.y + height.value ?? 0,
    x2: pos.value.x + width.value ?? 0,
    y2: targetPos.value?.y ?? 0,
  };
});

onMounted(() => {
  setTimeout(() => {
    const target = document.querySelector("[data-cta-target]");
    if (target) {
      targetEl.value = target as HTMLElement;
    } else {
      targetEl.value = null;
    }
  }, 1000);
});
</script>

<template>
  <div
    v-if="isVisible"
    ref="el"
    class="cta-presenter"
    :style="{ top: pos.y + 'px', left: pos.x + 1 + 'px' }"
  >
    (( CTA Presenter ))
    <!--
    <pre v-text="{ pos, targetPos, linePos }" />
    -->
  </div>
  <div
    v-if="isVisible"
    class="cta-marker"
    :style="{ top: targetPos.y + 'px', left: targetPos.x + 'px' }"
  />
  <div
    v-if="isVisible"
    class="cta-line"
    :style="{
      top: linePos.y1 + 'px',
      left: linePos.x1 + 'px',
      height: linePos.y2 - linePos.y1 + 'px',
    }"
  />
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.cta-presenter {
  position: fixed;
  min-width: 300px;
  min-height: 200px;
  z-index: 200;
  background: rgb(var(--c-green) / 100%);
  border-radius: 0.5rem 0.5rem 0;
  box-shadow: 2px 2px 10px rgb(0 0 0 / 10%);
}

.cta-marker {
  position: fixed;
  height: 5px;
  width: 5px;
  background: rgb(var(--c-green) / 100%);
  z-index: 200;
  border-radius: 50%;
}

.cta-line {
  position: fixed;
  height: 0;
  width: 0;
  z-index: 200;
  border-left: 1px solid rgb(var(--c-green) / 100%);
}
</style>
