<script type="ts">
import {
  computed,
  defineComponent, onMounted,
  ref,
  watch,
} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { storeToRefs } from "pinia";

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconClose from '@/components/ui/icon/IconClose.vue';
import IconFilter from '@/components/ui/icon/IconFilter.vue';
import IconSearch from '@/components/ui/icon/IconSearch.vue';
import { useAnalytics } from "@/composables/analytics";
import { useDevice } from "@/composables/device";
import { useUiStore } from "@/stores/ui";

export default defineComponent({
  components: {
    CircleButton,
    IconClose,
    IconSearch,
    IconFilter,
  },
  props: {
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
    hideFormForMobile: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const { filterExpanded } = storeToRefs(useUiStore());
    const { isDesktop } = useDevice();
    const { logUIEvent, logRawEvent } = useAnalytics();
    const isFormVisible = computed(() => {
      if (props.hideFormForMobile) {
        return isDesktop;
      }
      return true;
    })
    const toggleFilter = () => {
      filterExpanded.value = !filterExpanded.value;
      logUIEvent("searchbar:filter", filterExpanded.value ? "show" : "hide");
    };
    const q = ref('');
    const submitSearch = () => {
      const newQuery = { ...props.filter };
      if (q.value) {
        newQuery.q = q.value;
      } else {
        delete newQuery.q;
      }
      const routeName = route.name || 'discoverPlaylists';
      router.push({ name: routeName, query: newQuery });

      if (newQuery.q) {
        logRawEvent("view_search_results", {
          search_term: newQuery.q,
          filter_type: "search",
        });
      }
    };
    const searchInput = (e) => {
      if (e.code === 'Escape') {
        q.value = '';
        submitSearch();
        return;
      }
    };
    const clearSearch = () => {
      q.value = '';
      submitSearch();
    };
    const hasSearchQuery = computed(() => {
      return (props.filter && props.filter.q);
    });
    onMounted(() => {
      q.value = props.filter.q || '';
    });
    watch(
      () => props.filter,
      async (newFilter) => {
        q.value = newFilter.q;
      },
    );
    return {
      isDesktop,
      filterExpanded,
      isFormVisible,
      toggleFilter,
      q,
      searchInput,
      submitSearch,
      clearSearch,
      hasSearchQuery,
    };
  },
});
</script>
<template>
  <div class="searchbar">
    <form
      v-if="isFormVisible"
      class="search-input"
      :class="{
        'has-query': hasSearchQuery,
      }"
      @submit.prevent="submitSearch"
    >
      <input v-model="q" @keyup="searchInput" />
      <div v-if="hasSearchQuery" @click="clearSearch" class="clear-search">
        <IconClose color-var="--c-light" :scale="0.75" />
      </div>
    </form>
    <CircleButton v-if="isFormVisible" class="search-button" @click="submitSearch">
      <IconSearch />
    </CircleButton>
    <CircleButton
      class="filter-button"
      :filled="filterExpanded"
      :hover-background-opacity="filterExpanded ? '80%' : '10%'"
      @click="toggleFilter"
    >
      <IconFilter
        :color-var="filterExpanded ? `--c-light` : `--c-fg`"
        :rotate="filterExpanded ? 180 : 0"
      />
    </CircleButton>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.searchbar {
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: flex-end;

  .debug {
    position: fixed;
    left: 2rem;
  }

  .search-input {
    position: relative;
    height: 40px;

    > input {
      @include typo.default;

      box-sizing: border-box;
      height: 100%;
      padding: 3px 0.5rem 0 1rem;
      color: rgb(var(--c-page-fg));
      background: transparent;
      border: 0;
      border-bottom: 3px solid rgb(var(--c-page-fg) / 80%);
      transition: background 100ms, border 100ms, color 100ms, border-radius 100ms;

      &:focus {
        background: rgb(var(--c-dark) / 10%);
        border-bottom: 3px solid rgb(var(--c-page-fg) / 0%);
        outline: none;
      }
    }

    &.has-query {
      > input {
        color: rgb(var(--c-light));
        background: rgb(var(--c-dark));
        border-radius: 22px;
      }
    }

    .clear-search {
      top: 2px;
      position: absolute;
      height: 36px;
      width: 40px;
      right: 0;
      cursor: pointer;
    }
  }

  @include responsive.bp-medium {
    .search-button {
      order: -1;
    }

    .search-input {
      flex-grow: 1;

      > input {
        border: 1px solid rgb(var(--c-dark) / 20%);
        width: 100%;
      }
    }
  }
}
</style>
