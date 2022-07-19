<script type="ts">
import {
  computed,
  defineComponent, onMounted,
  ref,
  watch,
} from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconFilter from '@/components/ui/icon/IconFilter.vue';
import IconSearch from '@/components/ui/icon/IconSearch.vue';

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
  },
  setup(props) {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const isExpanded = computed(() => store.getters['ui/filterExpanded']);
    const toggleFilter = () => {
      if (isExpanded.value) {
        store.dispatch('ui/closeFilter');
      } else {
        store.dispatch('ui/expandFilter');
      }
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
      isExpanded,
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
      class="searchinput"
      :class="{
        'has-query': hasSearchQuery,
      }"
      @submit.prevent="submitSearch"
    >
      <input :value="q" @keyup="searchInput" />
    </form>
    <CircleButton :size="48" @click="submitSearch">
      <IconSearch :size="48" :color="`rgb(var(--c-page-fg))`" />
    </CircleButton>
    <CircleButton :size="48" :active="isExpanded" :color-var="`--c-black`" @click="toggleFilter">
      <IconFilter :size="48" :color="isExpanded ? `rgb(var(--c-white))` : `rgb(var(--c-black))`" />
    </CircleButton>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.searchbar {
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: flex-end;
}
.searchinput {
  height: 40px;
  > input {
    @include typo.default;
    //box-sizing: content-box;
    box-sizing: border-box;
    height: 100%;
    padding: 3px 0.5rem 0 1rem;
    color: rgb(var(--c-page-fg));
    background: transparent;
    border: 0;
    border-bottom: 3px solid rgba(var(--c-page-fg), 0.8);
    transition: background 100ms, border 100ms, color 100ms, border-radius 100ms;
    &:focus {
      background: rgba(var(--c-black), 0.1);
      border-bottom: 3px solid rgba(var(--c-page-fg), 0);
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
</style>
