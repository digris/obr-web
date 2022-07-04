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
  display: inline-flex;
  width: 20px;
  height: 20px;
  //background: rgba(20,255,20,0.5);
  background: rgb(var(--c-fg-inverse));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(var(--c-fg), 0.4);
  &__inner {
    width: 8px;
    height: 8px;
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
