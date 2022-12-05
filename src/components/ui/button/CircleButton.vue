<script lang="ts">
import { defineComponent } from "vue";

import { useIconSize } from "@/composables/icon";

export default defineComponent({
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: "--c-fg",
    },
    hoverBackgroundOpacity: {
      type: String,
      default: "10%",
    },
    outlined: {
      type: Boolean,
      default: false,
    },
    outlineOpacity: {
      type: String,
      default: "10%",
    },
    outlineWidth: {
      type: Number,
      default: 1,
    },
    outlineOnHover: {
      type: Boolean,
      default: false,
    },
    filled: {
      type: Boolean,
      default: false,
    },
    fillColorVar: {
      type: String,
      default: "--c-fg",
    },
    disabled: {
      type: Boolean,
      default: false,
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
      '--c-fill': `var(${fillColorVar})`,
      '--outline-opacity': outlineOpacity,
      '--outline-width': `${outlineWidth}px`,
      '--hover-background-opacity': hoverBackgroundOpacity,
      '--outline-hover-color': outlineOnHover ? 'rgba(var(--c-main)' : 'transparent',
    }"
    :class="{
      'is-outlined': outlined,
      'is-filled': filled,
      'is-disabled': disabled,
    }"
  >
    <slot name="default" />
    <div v-if="outlined" class="outline" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.circle-button {
  position: relative;
  height: var(--size);
  width: var(--size);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: var(--size);
  min-height: var(--size);
  border-radius: calc(var(--size) / 2);
  cursor: pointer;

  .outline {
    top: 0;
    position: absolute;
    height: 100%;
    width: 100%;
    left: 0;
    border: var(--outline-width) solid rgb(var(--c-main) / var(--outline-opacity));
    border-radius: calc(var(--size) / 2);
  }

  &.is-filled {
    background: rgb(var(--c-fill));
  }

  &.is-disabled {
    opacity: 0.2;
    pointer-events: none;
  }

  @include responsive.hover-supported {
    transition: background 1000ms, color 200ms, border 200ms;

    .outline {
      transition: inherit;
    }
  }

  @include responsive.on-hover {
    background: rgb(var(--c-main) / var(--hover-background-opacity));

    &.is-filled {
      background: rgb(var(--c-fill) / var(--hover-background-opacity));
    }

    .outline {
      border-color: var(--outline-hover-color);
    }
  }
}
</style>
