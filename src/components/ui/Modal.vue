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
    >
      <div
        v-if="isVisible"
        class="modal"
      >
        <div
          class="modal__header"
        >
          <h2
            class="title"
          >
            <slot
              name="title"
            />
          </h2>
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
  z-index: 4;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--c-black), 0.7);
  backdrop-filter: grayscale(70%) brightness(80%);
}
.modal {
  position: relative;
  z-index: 5;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: var(--container-width);
  min-height: calc(var(--container-width) / 2);
  color: rgb(var(--c-black));
  background: rgb(var(--c-white));

  &__header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 3rem;
    padding: 0 1rem;
    .title {
      flex-grow: 1;
    }
    .close-button {
      font-size: 1.5rem;
      background: transparent;
      border: none;
      cursor: pointer;
    }
  }
  &__body {
    display: flex;
    flex-direction: column;
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
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
