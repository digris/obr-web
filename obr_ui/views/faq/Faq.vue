<script lang="ts">
import { defineComponent, onActivated, ref } from "vue";
import { useI18n } from "vue-i18n";

import { getFaqCategories } from "@/api/faq";
import Topic from "@/components/faq/Topic.vue";
import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";
import type { Category } from "@/typings/api";

export default defineComponent({
  components: {
    Topic,
    SocialMediaLinks,
  },
  setup() {
    const { t } = useI18n();
    const categories = ref<Array<Category>>([]);
    onActivated(async () => {
      categories.value = await getFaqCategories();
    });
    return {
      t,
      categories,
    };
  },
});
</script>

<template>
  <div class="faq">
    <div class="title">
      <h1 v-text="t('menu.faq')" />
    </div>
    <div class="body">
      <section
        v-for="category in categories"
        :key="`faq-category-${category.uid}`"
        class="category"
      >
        <h2 v-text="category.name" />
        <div class="topics">
          <Topic v-for="topic in category.topics" :key="`faq-topic-${topic.uid}`" :topic="topic" />
        </div>
      </section>
    </div>
    <div class="appendix">
      <SocialMediaLinks v-if="categories.length" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/title";

.faq {
  @include container.small;

  .title {
    padding: 1.5rem 0;

    > h1 {
      @include typo.x-large;
      @include typo.bold;
    }
  }

  .body {
    .category {
      margin-bottom: 4rem;

      > h2 {
        @include typo.default;

        margin-bottom: 0.5rem;
      }
    }

    .topics {
      border-top: 1px solid rgb(var(--c-dark) / 20%);
    }
  }
}
</style>
