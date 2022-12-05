<script lang="ts">
import type { PropType } from "vue";
import { defineComponent } from "vue";

import type { SearchMediaResult } from "@/typings/api";

import Result from "./SearchResultsResult.vue";

export default defineComponent({
  components: {
    Result,
  },
  props: {
    results: {
      type: Array as PropType<Array<SearchMediaResult>>,
      default: () => [],
    },
  },
  emits: ["update:modelValue"],
  setup() {
    return {};
  },
});
</script>
<template>
  <div class="search-results">
    <Result
      v-for="(result, index) in results"
      :key="`search-result-${index}-${result.ct}-${result.uid}`"
      :result="result"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.search-results {
  background: transparent;

  > .search-result {
    border-bottom: 1px solid rgb(var(--c-gray-200));
  }
}
</style>
