<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, onActivated, onMounted, ref } from "vue";
import { whenever } from "@vueuse/core";
import { useRouteHash } from "@vueuse/router";
import showdown from "showdown";

import ExpandableSection from "@/components/ui/section/ExpandableSection.vue";
import type { Topic } from "@/typings/api";

const converter = new showdown.Converter();

export default defineComponent({
  components: {
    ExpandableSection,
  },
  props: {
    topic: {
      type: Object as PropType<Topic>,
      required: true,
    },
  },
  setup(props) {
    const hash = useRouteHash();
    const el = ref<HTMLAnchorElement | null>(null);
    const uid = computed(() => props.topic.uid);
    const isExpanded = computed(() => hash.value === `#${uid.value}`);
    const onExpand = () => (hash.value = `#${uid.value}`);
    const onCondense = () => (hash.value = "");
    const answerHtml = computed(() => converter.makeHtml(props.topic.answer));
    const scrollTo = () => {
      if (isExpanded.value && el.value) {
        // @ts-ignore
        el.value?.scrollIntoViewIfNeeded({
          block: "start",
          behavior: "smooth",
        });
      }
    };
    whenever(isExpanded, scrollTo);
    onActivated(() => scrollTo);
    onMounted(() => scrollTo);
    return {
      el,
      isExpanded,
      onExpand,
      onCondense,
      answerHtml,
    };
  },
});
</script>

<template>
  <ExpandableSection
    :is-expanded="isExpanded"
    @expand="onExpand"
    @condense="onCondense"
    class="topic"
  >
    <template #title>
      <a ref="el" :href="`#${topic.uid}`" @click.prevent v-text="topic.question" />
    </template>
    <div class="answer markdown" v-html="answerHtml" />
  </ExpandableSection>
</template>

<style lang="scss" scoped>
@use "@/style/elements/markdown";

.topic {
  border-top: 0;
  border-bottom: 1px solid rgb(var(--c-gray-200));

  &.is-expanded {
    color: rgb(var(--c-green));
  }

  :deep(.answer) {
    @include markdown.default;

    p {
      max-width: 800px;
    }
  }
}
</style>
