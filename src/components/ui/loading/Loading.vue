<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
  watch,
} from 'vue';
import { useElementVisibility } from '@vueuse/core';
import { debounce } from 'lodash-es';

import LoadingGrid from './LoadingGrid.vue';
import LoadingTable from './LoadingTable.vue';

const DEBOUNCE_FOR = 200;

export default defineComponent({
  props: {
    hasNext: {
      type: Boolean,
      default: false,
    },
    layout: {
      type: String,
      default: 'grid',
    },
  },
  emits: [
    'onEnter',
  ],
  setup(props, { emit }) {
    const root = ref(null);
    const inViewport = useElementVisibility(root);
    const onEnter = debounce(async () => {
      emit('onEnter');
    }, DEBOUNCE_FOR, { leading: true });
    watch(
      () => inViewport.value,
      (state) => {
        if (state) {
          onEnter();
        }
      },
    );
    const placeholder = computed(() => {
      return (props.layout === 'grid') ? LoadingGrid : LoadingTable;
    });
    return {
      root,
      onEnter,
      placeholder,
    };
  },
});
</script>
<template>
  <div
    ref="root"
    @enter="onEnter"
    class="loading-more"
  >
    <slot
      name="default"
    >
      <component
        :is="placeholder"
      />
    </slot>
  </div>
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
