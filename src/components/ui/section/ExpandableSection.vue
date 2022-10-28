<script lang="ts">
import { defineComponent } from "vue";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconPlus from "@/components/ui/icon/IconPlus.vue";
import IconMinus from "@/components/ui/icon/IconMinus.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconPlus,
    IconMinus,
  },
  props: {
    isExpanded: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["expand", "condense"],
  setup(props, { emit }) {
    const toggleExpanded = () => emit(props.isExpanded ? "condense" : "expand");
    return {
      toggleExpanded,
    };
  },
});
</script>

<template>
  <div class="expandable-section" :class="{ 'is-expanded': isExpanded }">
    <div @click="toggleExpanded" class="title">
      <div class="text">
        <slot name="title"></slot>
      </div>
      <CircleButton>
        <IconMinus v-if="isExpanded" />
        <IconPlus v-else />
      </CircleButton>
    </div>
    <div v-if="isExpanded" class="content">
      <slot name="default" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
.expandable-section {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;
  &.is-expanded {
    background: rgba(var(--c-black), 0.025);
  }
  .title {
    @include typo.large;
    min-height: calc(108px - 1rem);
    display: flex;
    align-items: center;
    cursor: pointer;
    .text {
      flex-grow: 1;
      padding-left: 0.5rem;
    }
  }
  .content {
    margin-bottom: 2rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  @include responsive.bp-medium {
    .title {
      min-height: calc(60px - 1rem);
    }
    .content {
      margin-top: 0.25rem;
      margin-bottom: 1rem;
    }
  }
}
</style>
