<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    tag: {
      type: Object,
      required: true,
    },
    selected: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'click',
  ],
  setup(props, { emit }) {
    const click = () => {
      emit('click', props.tag);
    };
    return {
      click,
    };
  },
});
</script>

<template>
  <div
    class="tag"
    @click.prevent="click"
    :class="{'is-selected': selected}"
  >
    {{ tag.name }}
    <small
      class="tag__type"
      v-text="tag.type"
    />
    <small
      class="tag__count"
      v-text="tag.count"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.tag {
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
  &__type {
    display: none;
    @include typo.tiny;
    @include typo.dim;
    padding-left: 0.5rem;
  }
  &__count {
    @include typo.tiny;
    @include typo.dim;
    padding-left: 0.5rem;
  }
}
</style>
