<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <transition name="fade">
    <div v-if="isVisible" class="playhead-handle">
      <div class="playhead-handle__inner" />
    </div>
  </transition>
</template>

<style lang="scss" scoped>
.playhead-handle {
  height: 20px;
  width: 20px;
  background: rgb(var(--c-fg-inverse));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(var(--c-fg) / 40%);

  &__inner {
    height: 8px;
    width: 8px;
    background: rgb(var(--c-fg));
    border-radius: 4px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>
