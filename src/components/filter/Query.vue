<script lang="ts">
import { defineComponent } from 'vue';

import IconRemove from '@/components/ui/icon/IconRemove.vue';

export default defineComponent({
  components: {
    IconRemove,
  },
  props: {
    q: {
      type: String,
      required: true,
    },
  },
  emits: [
    'click',
  ],
  setup(props, { emit }) {
    const click = () => {
      emit('click', props.q);
    };
    return {
      click,
    };
  },
});
</script>

<template>
  <div
    class="query is-selected"
    @click.prevent="click"
  >
    {{ q }}
    <IconRemove
      class="query__clear"
      color="rgb(var(--c-white))"
      :size="24"
    />
    <!--
    <small
      class="query__clear"
      v-text="`x`"
    />
    -->
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.query {
  display: inline-flex;
  align-items: center;
  height: 2rem;
  padding: 0.25rem 1rem;
  color: rgb(var(--c-black));
  text-transform: lowercase;
  background: rgb(var(--c-white));
  border: 1px solid rgba(var(--c-page-fg), 0.2);
  border-radius: 1rem;
  cursor: pointer;
  &:hover {
    background: rgb(var(--c-gray-100));
  }
  &.is-selected {
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
  }
  &__clear {
    margin-left: 0.5rem;
  }
}
</style>
