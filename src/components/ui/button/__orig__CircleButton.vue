<script lang="ts">
import { defineComponent } from "vue";

import { useIconSize } from "@/composables/icon";

export default defineComponent({
  props: {
    // size: {
    //   type: Number,
    //   default: 24,
    // },
    scale: {
      type: Number,
      default: 1,
    },
    outlined: {
      type: Boolean,
      default: false,
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
      default: "--c-page-fg",
    },
    activeColorVar: {
      type: String,
      default: "--c-page-fg-inverse",
    },
  },
  setup(props) {
    const { iconSize } = useIconSize(props.scale);
    return {
      iconSize,
    };
  },
});
</script>

<template>
  <div
    class="circle-button"
    :style="{
      '--icon-size': iconSize,
      '--size': `${iconSize}px`,
      '--c-main': `var(${colorVar})`,
      '--c-active': `var(${activeColorVar})`,
      '--outline-opacity': outlineOpacity,
      '--outline-width': `${outlineWidth}px`,
      '--outline-hover-color': outlineOnHover ? 'rgba(var(--c-main)' : 'transparent',
    }"
    :class="{
      'is-outlined': outlined,
      'has-shadow': hasShadow,
      'is-active': active,
      'is-filled': filled,
      'is-disabled': disabled,
    }"
  >
    <slot name="default" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.circle-button {
  height: var(--size);
  width: var(--size);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: var(--size);
  min-height: var(--size);
  border: var(--outline-width) solid transparent;
  border-radius: calc(var(--size) / 2);
  cursor: pointer;

  &.is-outlined {
    border-color: rgb(var(--c-main) var(--outline-opacity));
  }

  &.is-filled {
    background: rgb(var(--c-main));
  }

  &.is-active {
    color: rgb(var(--c-active));
    background: rgb(var(--c-main) 0.9);

    &:hover {
      background: rgb(var(--c-main) 0.7);
    }
  }

  &.is-disabled {
    opacity: 0.2;
    pointer-events: none;
  }

  &.has-shadow {
    box-shadow: rgb(var(--c-main) 0.2) 0 0 3px 0;
  }
  @include responsive.hover-supported {
    transition: background 1000ms, color 200ms, border 200ms;
  }
  @include responsive.on-hover {
    background: rgb(var(--c-main) 0.1);
    border-color: var(--outline-hover-color);
  }
  @include responsive.on-tap {
    background: rgb(var(--c-main) 0.1);
    border-color: var(--outline-hover-color);
  }
}
</style>
