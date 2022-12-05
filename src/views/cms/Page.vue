<script lang="ts">
import { defineComponent, onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";

import { getPage } from "@/api/cms";
import Section from "@/components/cms/Section.vue";
import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";
import type { Page } from "@/typings/api";

export default defineComponent({
  props: {
    path: {
      type: String,
      required: true,
    },
  },
  components: {
    Section,
    SocialMediaLinks,
  },
  setup(props) {
    const { t } = useI18n();
    const page = ref<Page | null>({});
    const loadPage = async (path: string) => {
      page.value = {};
      try {
        page.value = await getPage(path);
      } catch (err) {
        page.value = {
          title: t("pages.pageNotFound"),
          body: err?.message,
        };
      }
    };
    onBeforeMount(async () => {
      await loadPage(props.path);
    });
    watch(
      () => props.path,
      async (path) => {
        await loadPage(path);
      }
    );
    return {
      page,
    };
  },
});
</script>

<template>
  <div class="page">
    <div class="title" v-if="page.title">
      <h1 v-text="page.title" />
    </div>
    <div class="lead" v-if="page.lead" v-html="page.lead" />
    <div class="body">
      <Section
        v-for="section in page.sections"
        :key="`${section.ct}:${section.uid}`"
        :section="section"
      />
    </div>
    <div class="appendix">
      <SocialMediaLinks />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/cms";

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

    padding-bottom: 2rem;
    line-height: 120%;
  }

  .body {
    padding-top: 2rem;
    border-top: 1px solid rgb(var(--c-gray-200));
  }

  .appendix {
    padding: 2rem 0 6rem;
  }
}
</style>
