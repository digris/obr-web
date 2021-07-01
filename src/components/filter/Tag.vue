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
    >
      <small v-text="tag.type" />
    </small>
    <small
      class="tag__count"
    >
      <small v-text="tag.count" />
    </small>
  </div>
</template>

<style lang="scss" scoped>
.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 1rem;
  height: 2rem;
  border: 1px solid rgba(var(--c-live-fg), 0.2);
  border-radius: 1rem;
  color: rgb(var(--c-black));
  text-transform: lowercase;
  background: rgb(var(--c-white));
  cursor: pointer;
  &.is-selected {
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
  }
  &__type {
    //display: none;
    padding-left: 0.5rem;
    opacity: 0.5;
  }
  &__count {
    //display: none;
    padding-left: 0.5rem;
    opacity: 0.5;
  }
}
</style>
