<script lang="ts">
import {
  defineComponent,
  computed,
} from 'vue';

import SocialMediaLinks from '@/components/social-media/SocialMediaLinks.vue';

export default defineComponent({
  components: {
    SocialMediaLinks,
  },
  setup(props, { slots }) {
    const hasHeader = computed(() => !!slots.header);
    const hasBody = computed(() => !!slots.default);
    return {
      hasHeader,
      hasBody,
    };
  },
});
</script>

<template>
  <div
    class="detail"
  >
    <div
      v-if="hasHeader"
      class="detail__header"
    >
      <slot
        name="header"
      />
    </div>
    <section
      class="detail__body"
    >
      <slot
        name="default"
      />
    </section>
    <section
      class="detail__appendix"
    >
      <slot
        name="appendix"
      >
        <SocialMediaLinks />
      </slot>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.detail {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 78px);
  &__body {
    flex-grow: 1;
    background: rgb(var(--c-white));
  }
  &__appendix {
    padding: 2rem 0 6rem;
    background: rgb(var(--c-white));
  }
}
</style>
