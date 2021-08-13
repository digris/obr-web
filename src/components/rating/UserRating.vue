<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import IconHeart from '@/components/ui/icon/IconHeart.vue';

export default defineComponent({
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    iconSize: {
      type: Number,
      default: 24,
    },
  },
  components: {
    IconHeart,
  },
  setup(props) {
    const store = useStore();
    const userRating = computed(() => {
      return store.getters['rating/ratingByKey'](props.objKey);
    });
    const rate = async (value: number) => {
      const vote = {
        key: props.objKey,
        value,
      };
      await store.dispatch('rating/updateRating', vote);
    };
    return {
      userRating,
      rate,
    };
  },
});
</script>

<template>
  <div
    v-if="userRating"
    class="user-rating"
    :style="{
      height: `${iconSize}px`,
    }"
  >
    <IconHeart
      v-if="(userRating.value === 1)"
      :size="iconSize"
      @click="rate(null)"
      color="rgba(var(--c-page-fg), 0.8)"
    />
    <IconHeart
      v-if="(userRating.value === null)"
      :size="iconSize"
      :outlined="(true)"
      @click="rate(1)"
      color="rgba(var(--c-page-fg), 0.5)"
    />
    <span
      v-if="(userRating.value === -1)"
      @click="rate(null)"
    >
      -
    </span>
  </div>
</template>

<style lang="scss" scoped>
.user-rating {
  //background: red;
}
</style>
