<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, ref } from "vue";

import ExpandableSection from "@/components/ui/section/ExpandableSection.vue";
import type { Section } from "@/typings/api";

export default defineComponent({
  props: {
    section: {
      type: Object as PropType<Section>,
      required: true,
    },
  },
  components: {
    ExpandableSection,
  },
  setup(props) {
    const isExpanded = ref(false);
    const isExpandable = computed(() => {
      return !!(props.section.expandable && props.section.title);
    });
    return {
      isExpanded,
      isExpandable,
    };
  },
});
</script>

<template>
  <ExpandableSection
    v-if="isExpandable"
    :is-expanded="isExpanded"
    @expand="isExpanded = true"
    @condense="isExpanded = false"
    class="section"
  >
    <template #title>
      <h2 @click.prevent v-text="section.title" />
    </template>
    <div class="body" v-html="section.body" />
  </ExpandableSection>
  <section v-else class="section">
    <h2 v-if="section.title" class="title" v-text="section.title" />
    <div class="body" v-html="section.body" />
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/cms";

.section {
  .title {
    @include typo.large;
    @include typo.bold;

    margin: 0 0 0.5rem;
  }

  :deep(.body) {
    @include cms.content;
    @include cms.pyembed;

    > .toc {
      @include cms.toc;
    }

    > .admonition {
      @include cms.admonition;
    }

    > table {
      @include cms.table;
    }

    > .footnote {
      @include cms.footnote;
    }
  }
}

.expandable-section {
  :deep(.title) {
    @include typo.bold;
  }
}
</style>
