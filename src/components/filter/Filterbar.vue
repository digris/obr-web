<script type="ts">
import { computed, defineComponent } from 'vue';
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
  setup() {
    const store = useStore();
    const isExpanded = computed(() => store.getters['ui/filterExpanded']);
    const toggleFilter = () => {
      if (isExpanded.value) {
        store.dispatch('ui/closeFilter');
      } else {
        store.dispatch('ui/expandFilter');
      }
    };
    return {
      isExpanded,
      toggleFilter,
    };
  },
});
</script>
<template>
  <div
    class="filterbar"
  >
    <div
      class="searchinput"
    >
      <input />
    </div>
    <CircleButton
      :size="(48)"
      :outlined="(false)"
    >
      <IconSearch
        :size="(48)"
        :color="`rgb(var(--c-page-fg))`"
      />
    </CircleButton>
    <CircleButton
      :size="(48)"
      :outlined="(false)"
      :active="isExpanded"
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
.filterbar {
  display: flex;
  align-items: center;
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
