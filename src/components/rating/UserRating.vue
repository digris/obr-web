<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';

// import IconPlay from '@/components/ui/icon/IconPlay.vue';
import IconHeart from '@/components/ui/icon/IconHeart.vue';

export default defineComponent({
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
  },
  components: {
    IconHeart,
  },
  setup(props) {
    const store = useStore();
    const userRating = computed(() => {
      const rating = store.getters['rating/ratingByKey'](props.objKey);
      return rating;
    });
    const rate = async (value: number) => {
      console.debug('vote', value);
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
  >
    <IconHeart
      v-if="(userRating.value === 1)"
      :size="20"
      @click="rate(null)"
      color="rgba(var(--c-live-fg), 0.8)"
    />
    <IconHeart
      v-if="(userRating.value === null)"
      :size="20"
      :outlined="(true)"
      @click="rate(1)"
      color="rgba(var(--c-live-fg), 0.5)"
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
