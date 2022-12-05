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
  },
  setup(props, { slots }) {
    const hasLead = computed(() => !!slots.lead);
    return {
      hasLead,
    };
  },
});
</script>

<template>
  <div class="page">
    <div class="title">
      <h1 v-text="title" />
    </div>
    <div v-if="hasLead" class="lead">
      <slot name="lead" />
    </div>
    <div class="body">
      <slot name="default" />
    </div>
    <div class="appendix">
      <SocialMediaLinks />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";

.page {
  @include container.small;

  .title {
    padding: 1.5rem 0;

    > h1 {
      @include typo.x-large;
      @include typo.bold;
    }
  }

  .lead {
    @include typo.large;

    margin: 0 0 2rem;
    padding: 0 0 2rem;
    border-bottom: 1px solid rgb(var(--c-gray-200));
  }

  .body {
    background: inherit;
  }

  .appendix {
    padding: 2rem 0 6rem;
  }
}
</style>
