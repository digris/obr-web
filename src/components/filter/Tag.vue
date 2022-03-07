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
    <div
      class="tag__count"
    >
      <div
        class="tag__count__value"
        v-text="tag.count"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.tag {
  display: inline-flex;
  position: relative;
  align-items: center;
  height: 2.25rem;
  padding: 0.25rem 1rem;
  color: rgb(var(--c-black));
  text-transform: lowercase;
  background: rgba(var(--c-page-fg), 0.1);
  //border: 1px solid rgba(var(--c-page-fg), 0.2);
  border-radius: 1.125rem;
  cursor: pointer;
  &:hover {
    background: rgb(var(--c-gray-100));
    .tag__count {
      display: flex;
    }
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
    display: none;
    position: absolute;
    width: calc(100% - 2rem);
    bottom: 2rem;
    align-items: center;
    justify-content: center;
    &__value {
      background: #0004ff;
      color: #fff;
      width: 24px;
      height: 24px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
