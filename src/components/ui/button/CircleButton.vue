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
  //color: rgb(var(--c-live-bg));
  //background: rgba(var(--c-live-fg), 0.5);
  //border: none;
  border: 1px solid rgba(var(--c-live-fg), 0.2);
  border-radius: calc(var(--size) / 2);
  cursor: pointer;
  transition: background 100ms;
  &:hover {
    background: rgba(var(--c-live-fg), 0.9);
  }
}
</style>
