<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    // color: {
    //   type: String,
    //   default: 'rgb(var(--c-fg))',
    // },
    outlined: {
      type: Boolean,
      default: true,
    },
    active: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    backgroundColor: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        height: `${props.size}px`,
        width: `${props.size}px`,
        borderRadius: `${props.size / 2}px`,
      };
    });
    const cssVars = computed(() => {
      return {
        '--size': `${props.size}px`,
        '--c-circle-bg-color': props.backgroundColor,
      };
    });
    return {
      style,
      cssVars,
    };
  },
});
</script>

<template>
  <div
    class="circle-button"
    :style="cssVars"
    :class="{
      'is-outlined': outlined,
      'is-active': active,
      'is-disabled': disabled,
      'has-bg-color': backgroundColor,
    }"
  >
    <slot
      name="default"
    />
  </div>
</template>

<style lang="scss" scoped>
.circle-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--size);
  min-width: var(--size);
  height: var(--size);
  min-height: var(--size);
  border: 1px solid transparent;
  border-radius: calc(var(--size) / 2);
  cursor: pointer;
  transition: background 200ms, color 200ms, border 200ms;
  &:hover {
    background: rgba(var(--c-fg), 0.1);
    border-color: transparent;
  }
  &.has-bg-color {
    /* TODO: likley this could be implemented in a nicer way.. */
    background: var(--c-circle-bg-color);
  }
  &.is-outlined {
    border-color: rgba(var(--c-fg), 0.15);
  }
  &.is-active {
    background: rgb(var(--c-fg));
  }
  &.is-disabled {
    opacity: 0.8;
    pointer-events: none;
    > :deep(*) {
      opacity: 0.4;
    }
  }
}
</style>
