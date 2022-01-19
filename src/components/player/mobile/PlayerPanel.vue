<script lang="ts">
import {
  defineComponent,
} from 'vue';

import CloseButton from '@/components/ui/panel/CloseButton.vue';

export default defineComponent({
  components: {
    CloseButton,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    currentMedia: {
      type: Object,
    },
  },
  emits: [
    'close',
  ],
  setup(props, { emit }) {
    const close = () => {
      emit('close');
    };
    return {
      close,
    };
  },
});
</script>

<template>
  <transition
    name="slide"
  >
    <div
      v-if="isVisible"
      class="player-panel"
    >
      <div
        class="header"
      >
        <CloseButton
          @click="close"
        />
      </div>
      <div
        class="visual"
      >
        (( VISUAL ))
      </div>
      <div
        class="visual"
      >
        {{ currentMedia.name }}
      </div>
      <div
        class="playhead"
      >
        (( PLAYHEAD ))
      </div>
      <div
        class="controls"
      >
        (( CONTROLS ))
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
.player-panel {
  position: fixed;
  width: 100%;
  height: calc(100% - 60px);
  padding: 0.5rem;
  color: rgb(var(--c-fg));
  background: rgb(var(--c-bg));
  display: flex;
  flex-direction: column;
  align-items: center;
  .header {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    width: 100%;
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms, opacity 200ms;
}
.slide-enter-from {
  transform: translate(0, 100%);
  opacity: 0;
}
.slide-leave-to {
  transform: translate(0, 100%);
}
</style>
