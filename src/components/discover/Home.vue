<script lang="ts">
import { defineComponent, onMounted, watch } from "vue";

import MoodCard from "@/components/catalog/mood/Card.vue";
import { useCatalog } from "@/composables/catalog";
import { useRatingStore } from "@/stores/rating";

import HomeSection from "./HomeSection.vue";

export default defineComponent({
  components: {
    HomeSection,
    MoodCard,
  },
  setup() {
    const { moods, loadMoods } = useCatalog();
    const { injectRatings } = useRatingStore();
    onMounted(async () => {
      await loadMoods();
    });
    watch(() => moods.value, injectRatings);
    return {
      moods,
    };
  },
});
</script>

<template>
  <HomeSection title="Moods">
    <MoodCard v-for="mood in moods" :key="mood.uid" :mood="mood" />
  </HomeSection>
  <HomeSection title="Shows"> (( SHOWS )) </HomeSection>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/container";
@use "@/style/elements/grid";

section {
  @include container.default;

  margin-bottom: 2rem;
}
</style>
