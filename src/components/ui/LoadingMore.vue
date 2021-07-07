<script lang="ts">
import { debounce } from 'lodash-es';
import { defineComponent } from 'vue';
// @ts-ignore
import Intersect from '@/components/utils/intersect';

const DEBOUNCE_FOR = 100;

export default defineComponent({
  components: {
    Intersect,
  },
  props: {
    hasNext: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'onEnter',
  ],
  setup(props, { emit }) {
    const onEnter = debounce(async () => {
      emit('onEnter');
    }, DEBOUNCE_FOR, { leading: true });
    return {
      onEnter,
    };
  },
});
</script>
<template>
  <intersect
    @enter="onEnter"
    class="loading-more"
  >
    <span>loading</span>
  </intersect>
</template>

<style lang="scss" scoped>
.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 4rem;
  margin-top: 2rem;
}
</style>
