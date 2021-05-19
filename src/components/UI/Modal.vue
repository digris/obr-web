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
  <transition name="slide">
    <div
      v-if="isVisible"
      class="modal"
    >
      <div
        class="modal__header"
      >
        <button
          @click.prevent="close"
          class="close-button"
        >
          X
        </button>
      </div>
      <div
        class="modal__body"
      >
        <slot
          name="default"
        />
      </div>
      <div
        class="modal__footer"
      >
        <slot
          name="footer"
        />
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
.modal {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 5;
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
