<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { getMoods } from "@/api/catalog";

import MoodCard from "./Card.vue";

export default defineComponent({
  components: {
    MoodCard,
  },
  setup() {
    const moods = ref([]);
    const fetchMoods = async (limit = 16, offset = 0) => {
      const { results } = await getMoods(limit, offset);
      // @ts-ignore
      moods.value.push(...results);
    };
    onMounted(() => {
      fetchMoods();
    });
    return {
      moods,
    };
  },
});
</script>
<template>
  <div class="mood-list">
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
}
</style>
