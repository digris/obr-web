<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
  },
  setup(props) {
    const style = ref({
      height: `${props.size}px`,
      width: `${props.size}px`,
      borderRadius: `${props.size / 2}px`,
    });
    return {
      style,
    };
  },
});
</script>

<template>
  <div
    @click="increase"
    class="circle-button"
    :style="style"
  >
    <slot name="default" />
  </div>
</template>

<style lang="scss" scoped>
.circle-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: rgb(var(--c-live-bg));
  background: rgba(var(--c-live-fg), 0.5);
  border: none;
  cursor: pointer;
  transition: background 100ms;
  &:hover {
    background: rgba(var(--c-live-fg), 0.9);
  }
}
</style>
