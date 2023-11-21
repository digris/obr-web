<script lang="ts">
import { defineComponent } from "vue";

import IconRemove from "@/components/ui/icon/IconRemove.vue";

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
  emits: ["click"],
  setup(props, { emit }) {
    const click = () => {
      emit("click", props.q);
    };
    return {
      click,
    };
  },
});
</script>

<template>
  <div class="query is-selected" @click.prevent="click">
    {{ q }}
    <IconRemove class="query__clear" color-var="--c-light" :scale="0.5" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.query {
  display: inline-flex;
  align-items: center;
  height: 2rem;
  padding: 0.25rem 1rem;
  color: rgb(var(--c-dark) / 100%);
  text-transform: lowercase;
  background: rgb(var(--c-light) / 100%);
  border: 1px solid rgb(var(--c-page-fg) / 20%);
  border-radius: 1rem;
  cursor: pointer;

  &:hover {
    background: rgb(var(--c-dark) / 10%);
  }

  &.is-selected {
    color: rgb(var(--c-light));
    background: rgb(var(--c-dark));
  }

  &__clear {
    margin-left: 0.5rem;
  }
}
</style>
