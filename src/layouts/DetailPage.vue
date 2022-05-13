<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import { useElementSize } from "@vueuse/core";

import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";

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
    const hasHeader = computed(() => !!slots.header);
    const hasBody = computed(() => !!slots.default);
    const hasBackground = computed(() => !!slots.background);
    const headerEl = ref(null);
    const { height: headerHeight } = useElementSize(headerEl);
    const backgroundStyle = computed(() => {
      return {
        height: `${headerHeight.value + 300}px`,
      };
    });
    return {
      hasHeader,
      hasBody,
      hasBackground,
      headerEl,
      backgroundStyle,
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
  <div class="background" v-if="hasBackground" :style="backgroundStyle">
    <slot name="background" />
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
    background: transparent;
    :deep(.list-filter-container) {
      padding-left: 5rem;
    }
  }
  &__space {
    flex-grow: 1;
    min-height: 8rem;
    background: rgb(var(--c-white));
  }
  &__appendix {
    padding: 2rem 0 6rem;
    background: rgb(var(--c-white));
  }
}
.background {
  position: absolute;
  z-index: 1;
  top: -78px;
  width: 100%;
  overflow: hidden;
}
</style>
