<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";

import { getMoods } from "@/api/catalog";
import { usePullToRefresh } from "@/composables/pullToRefresh";
import { useRatingStore } from "@/stores/rating";

import MoodCard from "./Card.vue";

export default defineComponent({
  components: {
    MoodCard,
  },
  setup() {
    const { injectRatings } = useRatingStore();
    const moods = ref([]);
    const fetchMoods = async (limit = 16, offset = 0) => {
      const { results } = await getMoods(limit, offset);
      // @ts-ignore
      // moods.value.push(...results);
      moods.value = [...results];
      await injectRatings(results);
    };
    onMounted(() => {
      fetchMoods();
    });
    const listEl = ref();
    usePullToRefresh(listEl, fetchMoods);
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
