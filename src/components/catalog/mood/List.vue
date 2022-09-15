<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { usePullToRefresh } from "@/composables/pullToRefresh";
import { getMoods } from "@/api/catalog";

import MoodCard from "./Card.vue";

export default defineComponent({
  components: {
    MoodCard,
  },
  setup() {
    const store = useStore();
    const moods = ref([]);
    const fetchMoods = async (limit = 16, offset = 0) => {
      const { results } = await getMoods(limit, offset);
      // @ts-ignore
      // moods.value.push(...results);
      moods.value = [...results];

      // TODO: this kind of smells...
      await store.dispatch("rating/updateObjectRatings", results);
    };
    onMounted(() => {
      fetchMoods();
    });
    const listEl = ref();
    usePullToRefresh(listEl, fetchMoods);
    // usePullToRefresh(listEl, () => {
    //   return new Promise((resolve) => {
    //     fetchMoods().then(() => {
    //       resolve(true);
    //     });
    //   });
    // });
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
@use "@/style/elements/container";
@use "@/style/elements/grid";
.mood-list {
  @include container.default;
  margin-bottom: 0;
}
.grid {
  @include grid.default;
  grid-row-gap: 0.5rem;
}
</style>
