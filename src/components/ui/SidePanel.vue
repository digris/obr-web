<script lang="ts">
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'close',
  ],
  setup(props, { emit }) {
    const close = () => {
      emit('close');
    };
    onMounted(() => {
      document.addEventListener('keydown', (e) => {
        if (props.isVisible && e.code === 'Escape') {
          close();
        }
      });
    });
    return {
      close,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div
      v-if="isVisible"
      class="mask"
    />
  </transition>
  <transition name="slide">
    <div
      v-if="isVisible"
      class="side-panel"
    >
      <div
        class="side-panel__header"
      >
        <button
          @click.prevent="close"
          class="close-button"
        >
          X
        </button>
      </div>
      <div
        class="side-panel__body"
      >
        <slot
          name="default"
        />
      </div>
      <div
        class="side-panel__footer"
      >
        <slot
          name="footer"
        />
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
.mask {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  background: rgba(var(--c-black), 0.7);
  backdrop-filter: grayscale(70%) brightness(80%);
}
.side-panel {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 101;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 50vw;
  height: 100%;
  color: rgb(var(--c-black));
  background: rgb(var(--c-white));

  &__header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 3rem;
    padding-right: 1rem;
    .close-button {
      font-size: 1.5rem;
      background: transparent;
      border: none;
      cursor: pointer;
    }
  }
  &__body {
    flex-grow: 1;
    padding: 1rem;
  }
  &__footer {
    padding: 1rem;
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

.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms;
}
.slide-enter-from {
  transform: translate(100%, 0);
}
.slide-leave-to {
  transform: translate(100%, 0);
}
</style>
