<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    label: {
      type: String,
      required: true,
      default: "",
    },
  },
  emits: ["click"],
  setup(props, { emit }) {
    const onClick = () => {
      emit("click");
    };
    return {
      onClick,
    };
  },
});
</script>

<template>
  <div class="action" @click.prevent="onClick">
    <div class="action__icon">
      <slot name="icon"></slot>
    </div>
    <div class="action__name">
      <span v-text="label" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.action {
  display: flex;
  align-items: center;
  height: 3rem;
  border-bottom: 1px solid rgb(var(--c-gray-200));
  cursor: pointer;

  &:hover {
    background: rgb(var(--c-gray-100));
  }

  &__icon {
    height: 48px;
    width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__name {
    display: inline-flex;
    flex-grow: 1;
    align-items: center;
    justify-content: flex-start;
    height: 48px;
    padding-right: 1rem;

    > span {
      &::first-letter {
        text-transform: uppercase;
      }
    }
  }
}
</style>
