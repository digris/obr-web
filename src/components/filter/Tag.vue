<script lang="ts">
import { defineComponent } from "vue";

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
  emits: ["click"],
  setup(props, { emit }) {
    const click = () => {
      emit("click", props.tag);
    };
    return {
      click,
    };
  },
});
</script>

<template>
  <div class="tag" @click.prevent="click" :class="{ 'is-selected': selected }">
    {{ tag.name }}
    <small class="tag__type" v-text="tag.type" />
    <div class="tag__count">
      <div class="tag__count__value" v-text="tag.count" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";

.tag {
  position: relative;
  display: inline-flex;
  align-items: center;
  height: 2rem;
  padding: 0.25rem 1rem;
  color: rgb(var(--c-white));
  background: rgb(var(--c-white) / 20%);
  border-radius: 1rem;
  cursor: pointer;
  text-transform: capitalize;
  font-weight: 400;

  &.is-selected {
    color: rgb(var(--c-black));
    background: rgb(var(--c-white) / 100%);
  }

  &__type {
    display: none;
    padding-left: 0.5rem;
    @include typo.tiny;
    @include typo.dim;
  }

  &__count {
    @include typo.tiny;

    position: absolute;
    bottom: 2rem;
    display: none;
    align-items: center;
    justify-content: center;
    width: calc(100% - 2rem);

    &__value {
      height: 26px;
      width: 26px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgb(var(--c-white));
      color: rgb(var(--c-black));
      border: 1px solid rgb(var(--c-black) / 20%);
      border-radius: 12px;
    }
  }
  @include responsive.on-hover {
    background: rgb(var(--c-white) / 30%);

    .tag {
      &__count {
        display: flex;
      }
    }

    &.is-selected {
      background: rgb(var(--c-white) / 80%);
    }
  }
}
</style>
