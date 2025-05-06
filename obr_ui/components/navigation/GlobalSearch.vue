<script lang="ts">
import { defineComponent, ref } from "vue";
import { watchDebounced } from "@vueuse/core";

import { getGlobalMediaSearchResults } from "@/api/search";
import SearchInput from "@/components/search/SearchInput.vue";
import SearchResults from "@/components/search/SearchResults.vue";
import SidePanel from "@/components/ui/panel/SidePanel.vue";
import { useAnalytics } from "@/composables/analytics";
import eventBus from "@/eventBus";

export default defineComponent({
  components: {
    SidePanel,
    SearchInput,
    SearchResults,
  },
  setup() {
    const q = ref("");
    const results = ref([]);
    const resultsTotalCount = ref(0);
    const isVisible = ref(false);
    const close = () => (isVisible.value = false);
    const show = () => {
      isVisible.value = true;
    };
    eventBus.on("global-search:show", () => show());
    const { logRawEvent } = useAnalytics();
    watchDebounced(
      q,
      async (value: string) => {
        if (value) {
          const { count, results: searchResults } = await getGlobalMediaSearchResults(value, 10);
          resultsTotalCount.value = count;
          results.value = searchResults;
          logRawEvent("view_search_results", {
            search_term: value,
            filter_type: "global-search",
          });
        } else {
          resultsTotalCount.value = 0;
          results.value = [];
        }
      },
      {
        debounce: 500,
      }
    );
    return {
      q,
      results,
      isVisible,
      close,
    };
  },
});
</script>
<template>
  <SidePanel :is-visible="isVisible" @close="close">
    <template #header>
      <SearchInput v-model="q" />
    </template>
    <div class="global-search">
      <SearchResults v-if="results.length" :results="results" />
      <div v-if="results.length === 0" class="feedback">
        <i18n-t v-if="q" keypath="navigation.search.noResults" tag="p" />
        <i18n-t v-else keypath="navigation.search.cta" tag="p" />
        <i18n-t keypath="navigation.search.info" tag="p" />
      </div>
    </div>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.global-search {
  background: rgba(var(--c-light) / 100%);

  .feedback {
    padding: 0.5rem 0;
  }
}

.search-input {
  > input {
    @include typo.large;
    @include typo.bold;

    border: none;

    &:focus {
      outline: none;
    }

    &::placeholder {
      color: rgb(var(--c-dark) / 20%);
    }
  }
}

.search-results {
  border-top: 3px solid rgb(var(--c-dark));
  margin-top: -12px;

  @include responsive.bp-medium {
    margin-top: unset;
  }
}
</style>
