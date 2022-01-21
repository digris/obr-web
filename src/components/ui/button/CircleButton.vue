<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    hasShadow: {
      type: Boolean,
      default: false,
    },
    filled: {
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
    outlineOnHover: {
      type: Boolean,
      default: false,
    },
    colorVar: {
      type: String,
      default: '--c-page-fg',
    },
    activeColorVar: {
      type: String,
      default: '--c-page-fg-inverse',
    },
    progress: {
      type: Number,
      default: null,
    },
  },
});
</script>

<template>
  <div
    class="circle-button"
    :style="{
      '--size': `${size}px`,
      '--c-main': `var(${colorVar})`,
      '--c-active': `var(${activeColorVar})`,
      '--outline-opacity': outlineOpacity,
      '--outline-width': `${outlineWidth}px`,
      '--outline-hover-color': outlineOnHover ? 'rgba(var(--c-main)': 'transparent',
    }"
    :class="{
      'is-outlined': outlined,
      'has-shadow': hasShadow,
      'is-active': active,
      'is-filled': filled,
      'is-disabled': disabled,
      'is-progress': progress !== null,
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
  border: var(--outline-width) solid transparent;
  border-radius: calc(var(--size) / 2);
  cursor: pointer;
  transition: background 200ms, color 200ms, border 200ms;
  &.is-outlined {
    border-color: rgba(var(--c-main), var(--outline-opacity));
  }
  &.is-filled {
    background: rgb(var(--c-main));
  }
  &.is-active {
    color: rgb(var(--c-active));
    background: rgba(var(--c-main), 0.9);
    &:hover {
      background: rgba(var(--c-main), 0.7);
    }
  }
  &.is-disabled {
    opacity: 0.2;
    pointer-events: none;
  }
  &.has-shadow {
    box-shadow: rgba(var(--c-main), 0.2) 0 0 3px 0;
  }
  &:hover {
    background: rgba(var(--c-main), 0.1);
    border-color: var(--outline-hover-color);
  }
}
</style>
