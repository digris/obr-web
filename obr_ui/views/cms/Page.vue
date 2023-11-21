<script lang="ts">
import { defineComponent, nextTick, onBeforeMount, ref, watch } from "vue";
import { useI18n } from "vue-i18n";

import { getPage } from "@/api/cms";
import Section from "@/components/cms/Section.vue";
import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";
import { useSettings } from "@/composables/settings";
import type { Page } from "@/typings/api";

interface ErrorPage {
  title: string;
  message: string;
}

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
    const { locale } = useSettings();
    const page = ref<Page | null>(null);
    const errorPage = ref<ErrorPage | null>(null);
    const loadPage = async (path: string) => {
      page.value = null;
      errorPage.value = null;
      try {
        page.value = await getPage(path);
        errorPage.value = null;
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "";
        errorPage.value = {
          title: t("pages.pageNotFound"),
          message,
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
    watch(
      () => locale.value,
      () => {
        nextTick(() => {
          loadPage(props.path);
        });
      }
    );
    return {
      page,
      errorPage,
    };
  },
});
</script>

<template>
  <div v-if="errorPage" class="page has-error">
    <div class="title">
      <h1 v-text="errorPage.title" />
    </div>
    <div class="lead" v-if="errorPage.message" v-html="errorPage.message" />
  </div>
  <div v-if="page" class="page">
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
@use "@/style/base/responsive";
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

    @include responsive.bp-medium {
      padding: 0.625rem 0 1rem;
    }
  }

  .lead {
    @include typo.large;

    padding-bottom: 2rem;
    line-height: 120%;
  }

  .body {
    padding-top: 2rem;
    border-top: 1px solid rgb(var(--c-dark) / 20%);
  }

  .appendix {
    padding: 2rem 0 6rem;
  }
}
</style>
