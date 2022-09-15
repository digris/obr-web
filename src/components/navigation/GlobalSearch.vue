<script lang="ts">
import { defineComponent, ref, nextTick, watch } from "vue";
import { useI18n } from "vue-i18n";
import { getGlobalSearchResults } from "@/api/search";
import eventBus from "@/eventBus";
import SidePanel from "@/components/ui/panel/SidePanel.vue";

export default defineComponent({
  components: {
    SidePanel,
  },
  setup() {
    const { t } = useI18n();
    const q = ref("");
    const results = ref([]);
    const searchInput = ref<HTMLInputElement | null>(null);
    const isVisible = ref(false);
    const close = () => (isVisible.value = false);
    const show = () => {
      isVisible.value = true;
      nextTick(() => {
        if (searchInput.value) {
          searchInput.value.focus();
        }
      });
    };
    eventBus.on("global-search:show", () => show());
    watch(
      () => q.value,
      async (value) => {
        results.value = await getGlobalSearchResults(value);
      }
    );
    return {
      t,
      q,
      results,
      searchInput,
      isVisible,
      close,
    };
  },
});
</script>
<template>
  <SidePanel :is-visible="isVisible" @close="close">
    <template #header>
      <div class="search-input">
        <input ref="searchInput" v-model="q" type="text" :placeholder="t('search.search')" />
      </div>
    </template>
    <div class="global-search">
      <div v-if="results.length" class="search-results">
        <pre v-text="results" />
      </div>
      <div class="feedback">
        <p>
          Durchsuche das open broadcast Archiv.<br />
          Du kannst nach Tracks, Releases oder Künsternamem suchen.
        </p>
      </div>
    </div>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.global-search {
  background: white;
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
      color: rgba(var(--c-black), 0.2);
    }
  }
}
</style>
