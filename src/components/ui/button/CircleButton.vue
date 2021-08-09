<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    backgroundColor: {
      type: String,
      default: 'rgb(var(--c-live-fg))',
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    hasShadow: {
      type: Boolean,
      default: false,
    },
    active: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    outlineOpacity: {
      type: Number,
      default: 0.1,
    },
    outlineWidth: {
      type: Number,
      default: 1,
    },
  },
  setup(props) {
    const style = computed(() => {
      return {
        height: `${props.size}px`,
        width: `${props.size}px`,
        borderRadius: `${props.size / 2}px`,
      };
      // backgroundColor: props.backgroundColor,
    });
    const cssVars = computed(() => {
      return {
        '--size': `${props.size}px`,
        '--outline-opacity': props.outlineOpacity,
        '--outline-width': `${props.outlineWidth}px`,
      };
      // backgroundColor: props.backgroundColor,
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
      'has-shadow': hasShadow,
      'is-active': active,
      'is-disabled': disabled,
    }"
  >
    <slot name="default" />
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
  border: var(--outline-width) solid transparent;
  border-radius: calc(var(--size) / 2);
  cursor: pointer;
  transition: background 200ms, color 200ms, border 200ms;
  &.is-outlined {
    border-color: rgba(var(--c-live-fg), var(--outline-opacity));
  }
  &.has-shadow {
    box-shadow: rgba(var(--c-live-fg), 0.2) 0 0 3px 0;
  }
  &.is-active {
    color: rgb(var(--c-live-fg-inverse));
    background: rgb(var(--c-live-fg));
  }
  &.is-disabled {
    opacity: 0.2;
    pointer-events: none;
  }
  &:hover {
    background: rgba(var(--c-live-fg), 0.1);
    border-color: transparent;
  }
}
</style>
