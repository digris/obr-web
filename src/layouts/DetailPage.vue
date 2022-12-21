<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useElementSize } from "@vueuse/core";

import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";
import { useDevice } from "@/composables/device";

export default defineComponent({
  components: {
    SocialMediaLinks,
  },
  props: {
    appendixVisible: {
      type: Boolean,
      default: true,
    },
  },
  setup(props, { slots }) {
    const { isApp } = useDevice();
    const hasHeader = computed(() => !!slots.header);
    const hasBody = computed(() => !!slots.default);
    const hasBackground = computed(() => !!slots.background);
    const headerEl = ref(null);
    const { height: headerElHeight, width: headerWidth } = useElementSize(headerEl);
    const headerHeight = computed(() => {
      if (isApp) {
        return headerElHeight.value + 140;
      }
      return headerElHeight.value + 68;
    });
    return {
      hasHeader,
      hasBody,
      hasBackground,
      headerEl,
      headerHeight,
      headerWidth,
    };
  },
});
</script>

<template>
  <div class="detail">
    <div ref="headerEl" v-if="hasHeader" class="detail__header">
      <slot name="header" />
    </div>
    <section class="detail__body">
      <slot name="default" />
    </section>
    <section class="detail__space" />
    <section class="detail__appendix">
      <slot name="appendix">
        <SocialMediaLinks v-if="appendixVisible" />
      </slot>
    </section>
  </div>
  <div class="background" v-if="hasBackground">
    <slot name="background" :width="headerWidth" :height="headerHeight" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

.detail {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 78px);

  &__header {
    background: transparent;
  }

  &__body {
    background: rgb(var(--c-light) / 100%);
  }

  &__space {
    flex-grow: 1;
    min-height: 4rem;
    background: rgb(var(--c-light) / 100%);
  }

  &__appendix {
    padding: 2rem 0 6rem;
    background: rgb(var(--c-light) / 100%);
  }
}

.background {
  top: 0;
  position: absolute;
  width: 100%;
  z-index: 1;
  overflow: hidden;
}
</style>
