<script lang="ts">
import { computed, defineComponent } from "vue";

import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";

export default defineComponent({
  components: {
    SocialMediaLinks,
  },
  props: {
    title: {
      type: String,
      default: "",
    },
    appendixVisible: {
      type: Boolean,
      default: true,
    },
  },
  setup(props, { slots }) {
    const hasLead = computed(() => !!slots.lead);
    const hasBody = computed(() => !!slots.default);
    return {
      hasLead,
      hasBody,
    };
  },
});
</script>

<template>
  <div class="page">
    <div class="title" v-if="title">
      <h1 v-text="title" />
    </div>
    <div v-if="hasLead" class="lead">
      <slot name="lead" />
    </div>
    <div class="body">
      <slot name="default" />
    </div>
    <div v-if="appendixVisible" class="appendix">
      <SocialMediaLinks />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";

.page {
  @include container.small;

  .title {
    padding: 1.5rem 0;

    > h1 {
      @include typo.x-large;
      @include typo.bold;
    }

    @include responsive.bp-medium {
      padding: 0.625rem 0 1rem;
    }
  }

  .lead {
    @include typo.large;

    padding-bottom: 2rem;
    line-height: 120%;
  }

  /*
  .body {
    background: yellow;
  }
  */

  .appendix {
    padding: 2rem 0 6rem;
  }
}
</style>
