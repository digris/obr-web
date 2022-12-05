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
import IconFilter from '@/components/ui/icon/IconFilter.vue';
import IconSearch from '@/components/ui/icon/IconSearch.vue';
import { useDevice } from "@/composables/device";
import { useUiStore } from "@/stores/ui";

export default defineComponent({
  components: {
    CircleButton,
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
    const isFormVisible = computed(() => {
      if (props.hideFormForMobile) {
        return isDesktop.value;
      }
      return true;
    })
    const toggleFilter = () => {
      filterExpanded.value = !filterExpanded.value;
    };
    const q = ref('');
    const submitSearch = () => {
      const newQuery = { ...props.filter };
      newQuery.q = q.value;
      const routeName = route.name || 'discoverPlaylists';
      router.push({ name: routeName, query: newQuery });
    };
    const searchInput = (e) => {
      if (e.code === 'Escape') {
        e.target.value = '';
        q.value = '';
        submitSearch();
        return;
      }
      q.value = e.target.value;
    };
    const hasSearchQuery = computed(() => {
      return (props.filter && props.filter.q);
      // return true;
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
      <input :value="q" @keyup="searchInput" />
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
        :color-var="filterExpanded ? `--c-white` : `--c-fg`"
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

  .search-input {
    height: 40px;

    > input {
      @include typo.default;

      box-sizing: border-box;
      height: 100%;
      padding: 3px 0.5rem 0 1rem;
      color: rgb(var(--c-page-fg));
      background: transparent;
      border: 0;
      border-bottom: 3px solid rgb(var(--c-page-fg) 0.8);
      transition: background 100ms, border 100ms, color 100ms, border-radius 100ms;

      &:focus {
        background: rgb(var(--c-black) 0.1);
        border-bottom: 3px solid rgb(var(--c-page-fg) 0);
        outline: none;
      }
    }

    &.has-query {
      > input {
        color: rgb(var(--c-white));
        background: rgb(var(--c-black));
        border-radius: 22px;
      }
    }
  }
  @include responsive.bp-medium {
    .search-button {
      order: -1;
    }

    .search-input {
      flex-grow: 1;

      > input {
        border: 1px solid rgb(var(--c-gray-200));
        width: 100%;
      }
    }
  }
}
</style>
