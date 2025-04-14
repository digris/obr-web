<script lang="ts" setup>
import { computed, onActivated, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useEventListener, whenever } from "@vueuse/core";
import { useRouteHash } from "@vueuse/router";
import showdown from "showdown";

import { type AnalyticsEvent, sendEvent } from "@/analytics/event";
import ExpandableSection from "@/components/ui/section/ExpandableSection.vue";
import type { Topic } from "@/typings/api";

const props = defineProps<{
  topic: Topic;
}>();

const converter = new showdown.Converter({
  openLinksInNewWindow: true,
});

const router = useRouter();
const hash = useRouteHash();
const linkEl = ref<HTMLAnchorElement | null>(null);
const uid = computed(() => props.topic.uid);
const isExpanded = computed(() => hash.value === `#${uid.value}`);
const onExpand = () => {
  hash.value = `#${uid.value}`;
  const evt = {
    kind: "faq:expand",
    data: {
      topic: props.topic.question,
    },
  } as AnalyticsEvent;
  sendEvent(evt);
};
const onCondense = () => (hash.value = "");
const answerHtml = computed(() => converter.makeHtml(props.topic.answer));

// override link handling
const answerEl = ref<HTMLElement | null>(null);
useEventListener(answerEl, "click", (e) => {
  const origin = (e.target as Element).closest("a");
  const href = origin?.getAttribute("href");
  if (!href) {
    return;
  }
  if (href.startsWith("/")) {
    console.debug("FAQ: internal link - navigate via router", href);
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    router.push(href);
  }
});

const scrollTo = () => {
  if (isExpanded.value && linkEl.value) {
    // @ts-ignore
    linkEl.value?.scrollIntoViewIfNeeded({
      block: "start",
      behavior: "smooth",
    });
  }
};
whenever(isExpanded, scrollTo);
onActivated(scrollTo);
onMounted(scrollTo);
</script>

<template>
  <ExpandableSection
    :is-expanded="isExpanded"
    @expand="onExpand"
    @condense="onCondense"
    class="topic"
  >
    <template #title>
      <a ref="linkEl" :href="`#${topic.uid}`" @click.prevent v-text="topic.question" />
    </template>
    <div ref="answerEl" class="answer markdown" v-html="answerHtml" />
  </ExpandableSection>
</template>

<style lang="scss" scoped>
@use "@/style/elements/markdown";

.topic {
  border-top: 0;
  border-bottom: 1px solid rgb(var(--c-dark) / 20%);

  &.is-expanded {
    color: rgb(var(--c-green) / 100%);
  }

  :deep(.answer) {
    @include markdown.default;

    p {
      max-width: 800px;
    }
  }
}
</style>
