<script type="ts">
import { ref, computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconSearch from '@/components/ui/icon/IconSearch.vue';
import IconHashtag from '@/components/ui/icon/IconHashtag.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconSearch,
    IconHashtag,
  },
  props: {
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
  emits: [
    'change',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const isExpanded = computed(() => store.getters['ui/filterExpanded']);
    const toggleFilter = () => {
      if (isExpanded.value) {
        store.dispatch('ui/closeFilter');
      } else {
        store.dispatch('ui/expandFilter');
      }
    };
    const query = ref('');
    const searchInput = (e) => {
      query.value = e.target.value;
    };
    const updateSearchQuery = () => {
      const filter = { ...props.filter };
      filter.q = query.value;
      emit('change', filter);
    };
    return {
      isExpanded,
      toggleFilter,
      query,
      searchInput,
      updateSearchQuery,
    };
  },
});
</script>
<template>
  <div
    class="searchbar"
  >
    <div
      class="searchinput"
    >
      <input
        :value="filter.q"
        @keyup="searchInput"
      />
    </div>
    <CircleButton
      :size="(48)"
      :outlined="(false)"
      @click="updateSearchQuery"
    >
      <IconSearch
        :size="(48)"
        :color="`rgb(var(--c-page-fg))`"
      />
    </CircleButton>
    <CircleButton
      :size="(48)"
      :outlined="(false)"
      :active="(isExpanded)"
      :color-var="`--c-black`"
      @click="toggleFilter"
    >
      <IconHashtag
        :size="(48)"
        :color="(isExpanded ? `rgb(var(--c-page-bg))` : `rgb(var(--c-page-fg))`)"
      />
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
    box-sizing: content-box;
    height: 100%;
    color: rgb(var(--c-page-fg));
    background: transparent;
    border: 0;
    border-bottom: 3px solid rgba(var(--c-page-fg), 0.8);
    &:focus {
      border-bottom: 3px solid rgb(var(--c-page-fg));
      outline: none;
    }
  }
}
</style>
