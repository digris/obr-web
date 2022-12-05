<script lang="ts">
import { computed, defineComponent } from "vue";

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
    outlineWidth: {
      type: Number,
      default: 1,
    },
    outlineOpacity: {
      type: String,
      default: "15%",
    },
    active: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    inactive: {
      type: Boolean,
      default: false,
    },
    backgroundColor: {
      type: String,
      default: null,
    },
    hoverBackgroundColor: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const { iconSize } = useIconSize(props.scale);
    const style = computed(() => {
      return {
        // height: `${iconSize.value}px`,
        // width: `${iconSize.value}px`,
        // borderRadius: `${iconSize.value / 2}px`,
      };
    });
    const cssVars = computed(() => {
      return {
        "--size": `${iconSize.value}px`,
        "--c-circle-bg-color": props.backgroundColor,
        "--outline-width": `${props.outlineWidth}px`,
        "--outline-opacity": props.outlineOpacity,
        "--hover-bg-color": props.hoverBackgroundColor,
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
      'is-inactive': inactive,
      'has-bg-color': backgroundColor,
      'has-hover-bg-color': hoverBackgroundColor,
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
  transition: background 200ms, color 200ms, border 200ms;

  &.has-bg-color {
    /* TODO: likley this could be implemented in a nicer way.. */
    background: var(--c-circle-bg-color);
  }

  &.is-outlined {
    border-color: rgb(var(--c-fg) / var(--outline-opacity));
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

  &.is-inactive {
    opacity: 0.8;

    > :deep(*) {
      opacity: 0.4;
    }
  }
  @include responsive.on-hover {
    background: rgb(var(--c-fg) 0.15);
    border-color: transparent;

    &.is-outlined {
      border-color: transparent;
    }

    &.has-hover-bg-color {
      background: var(--hover-bg-color);
    }
  }
}
</style>
