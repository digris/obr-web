<script lang="ts">
import {
  computed,
  defineComponent,
  watch,
  onMounted,
} from 'vue';
import { useStore } from 'vuex';

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconHeart from '@/components/ui/icon/IconHeart.vue';
import IconFlash from '@/components/ui/icon/IconFlash.vue';

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  components: {
    CircleButton,
    IconHeart,
    IconFlash,
  },
  setup(props) {
    const store = useStore();
    const objKey = computed(() => {
      return `${props.media.ct}:${props.media.uid}`;
    });
    const userRating = computed(() => {
      return store.getters['rating/ratingByKey'](objKey.value);
    });
    const userRatingValue = computed(() => {
      return userRating.value?.value;
    });
    const rate = async (value: number) => {
      const vote = {
        key: objKey.value,
        value: userRatingValue.value === value ? null : value,
      };
      await store.dispatch('rating/updateRating', vote);
    };
    const fetchRating = async (key: string) => {
      if (!key) {
        return;
      }
      if (userRating.value) {
        return;
      }
      await store.dispatch('rating/loadRating', key);
    };
    onMounted(() => {
      fetchRating(objKey.value);
    });
    watch(objKey, async (key) => {
      await fetchRating(key);
    });
    return {
      userRating,
      userRatingValue,
      rate,
    };
  },
});
</script>

<template>
  <div
    class="rating"
  >
    <div
      class="total"
    >
      ?
    </div>
    <div>
      <CircleButton
        :size="48"
        @click="rate(1)"
      >
        <IconHeart
          :size="28"
          :outlined="(userRatingValue !== 1)"
          color="rgb(var(--c-page-fg))"
        />
      </CircleButton>
    </div>
    <div>
      <CircleButton
        :size="48"
        :active="(userRatingValue === -1)"
      >
        <IconFlash
          :size="42"
          @click="rate(-1)"
          :outlined="(true)"
          :color="`rgb(var(--c-live-${userRatingValue === -1 ? 'bg' : 'fg'}))`"
        />
      </CircleButton>
    </div>
    <div
      class="total"
    >
      ?
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.rating {
  display: grid;
  grid-template-columns: repeat(4, 4rem);
  > div {
    align-self: center;
    justify-self: center;
  }
  .total {
    @include typo.dim;
    @include typo.light;
    opacity: 0;
  }
}
</style>
