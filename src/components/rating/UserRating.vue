<script lang="ts">
import {
  computed,
  defineComponent,
  onMounted,
} from 'vue';
import { useStore } from 'vuex';

import IconHeart from '@/components/ui/icon/IconHeart.vue';
import IconFlash from '@/components/ui/icon/IconFlash.vue';

export default defineComponent({
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    autoload: {
      type: Boolean,
      default: false,
    },
    iconSize: {
      type: Number,
      default: 48,
    },
    colorVar: {
      type: String,
      default: '--c-black',
    },
    hideIfUnset: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    IconHeart,
    IconFlash,
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
    const style = computed(() => {
      return {
        height: `${props.iconSize}px`,
        opacity: (props.hideIfUnset && userRating.value.value === null) ? 0 : 1,
      };
    });
    onMounted(() => {
      if (props.autoload) {
        store.dispatch('rating/loadRating', props.objKey);
      }
    });
    return {
      userRating,
      rate,
      style,
    };
  },
});
</script>

<template>
  <div
    v-if="userRating"
    class="user-rating"
    :style="style"
  >
    <IconHeart
      v-if="(userRating.value === 1)"
      :size="iconSize"
      @click="rate(null)"
      :color="`rgba(var(${colorVar}), 0.8)`"
    />
    <IconHeart
      v-if="(userRating.value === null)"
      :size="iconSize"
      :outlined="(true)"
      @click="rate(1)"
      :color="`rgba(var(${colorVar}), 0.5)`"
    />
    <IconFlash
      v-if="(userRating.value === -1)"
      :size="iconSize"
      @click="rate(null)"
    />
  </div>
</template>

<style lang="scss" scoped>
.user-rating {
  transition: opacity 200ms ease-in-out;
}
</style>
