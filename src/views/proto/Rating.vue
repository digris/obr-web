<script lang="ts">
import { defineComponent, ref, computed, onActivated } from "vue";
import { useRatingStore } from "@/stores/rating";

export default defineComponent({
  components: {},
  setup() {
    const objKey = ref("catalog.playlist:9255A232");
    const { ratingByKey, loadRating, setRating } = useRatingStore();
    // const vote = voteByObjKey(objKey.value);
    // const rating = computed(() => {
    //   return ratingByObjKey(objKey.value);
    // });
    const rating = computed({
      // @ts-ignore
      get() {
        return ratingByKey(objKey.value);
      },
      async set(value: number | null) {
        // Note: we are using destructuring assignment syntax here.
        await setRating(objKey.value, value);
      },
    });
    onActivated(async () => {
      if (rating.value === undefined) {
        await loadRating(objKey.value);
      }
    });
    return {
      objKey,
      rating,
    };
  },
});
</script>
<template>
  <div class="stage">
    <h1>?</h1>
    <input v-model="objKey" :style="{ minWidth: '200px' }" />
    <pre
      v-text="{
        objKey,
        rating,
      }"
    />
    <div>
      <button @click="rating = 1">+1</button>
      <button @click="rating = null">null</button>
      <button @click="rating = -1">-1</button>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.stage {
  padding: 2rem;
}
</style>
