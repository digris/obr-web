<script lang="ts">
import { defineComponent, onMounted, ref, watch } from "vue";

import { useCatalog } from "@/composables/catalog";
import { usePullToRefresh } from "@/composables/pullToRefresh";
import { useRatingStore } from "@/stores/rating";

import MoodCard from "./Card.vue";

export default defineComponent({
  components: {
    MoodCard,
  },
  setup() {
    const { moods, loadMoods } = useCatalog();
    const { injectRatings } = useRatingStore();
    onMounted(async () => {
      await loadMoods();
    });
    // watch(
    //   () => moods.value,
    //   async (value) => {
    //     await injectRatings(value);
    //   }
    // );
    watch(() => moods.value, injectRatings);
    const listEl = ref();
    usePullToRefresh(listEl, loadMoods);
    return {
      listEl,
      moods,
    };
  },
});
</script>
<template>
  <div ref="listEl" class="mood-list">
    <div class="grid">
      <MoodCard v-for="mood in moods" :key="mood.uid" :mood="mood" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/container";
@use "@/style/elements/grid";

.mood-list {
  @include container.default;

  margin-bottom: 4rem;
}

.grid {
  @include grid.default;

  grid-row-gap: 0.5rem;
  @include responsive.bp-medium {
    grid-row-gap: 0.625rem;
  }
}
</style>
