<script lang="ts">
import { defineComponent, onMounted, onUpdated, ref } from "vue";

export default defineComponent({
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
  setup(props, { slots, emit }) {
    const close = () => {
      emit("close");
    };
    const hasFeedback = ref(false);
    const feedbackClass = ref("is-info");

    onUpdated(() => {
      hasFeedback.value = !!(slots.warning || slots.success || slots.info);
      if (slots.warning) {
        feedbackClass.value = "is-warning";
      }
      if (slots.success) {
        feedbackClass.value = "is-success";
      }
    });

    onMounted(() => {
      document.addEventListener("keydown", (e) => {
        if (props.isVisible && e.code === "Escape") {
          close();
        }
      });
    });
    return {
      close,
      hasFeedback,
      feedbackClass,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" class="mask">
      <div v-if="isVisible" class="modal">
        <div class="modal__header">
          <h2 class="title">
            <slot name="title" />
          </h2>
          <button @click.prevent="close" class="close-button">X</button>
        </div>
        <div class="modal__body">
          <slot name="default" />
        </div>
        <div class="modal__footer">
          <slot name="footer" />
        </div>
        <!-- full-screen overlay for feedback (errors / success / info) -->
        <transition name="fade">
          <div v-if="hasFeedback" class="modal__feedback" :class="feedbackClass">
            <slot name="warning" />
            <slot name="success" />
            <slot name="info" />
          </div>
        </transition>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

$z-mask: 4;
$z-modal: 5;
$z-header: 10;
$z-feedback: 9;

.mask {
  top: 0;
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: $z-mask;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(var(--c-black) 0.7);
  backdrop-filter: grayscale(70%) brightness(80%);
}

.modal {
  position: relative;
  z-index: $z-modal;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: var(--container-width);
  min-height: calc(var(--container-width) / 1.75);
  color: rgb(var(--c-black));
  background: rgb(var(--c-white));

  @include responsive.bp-medium {
    height: 100%;
  }

  &__header {
    z-index: $z-header;
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

  &__feedback {
    top: 0;
    position: absolute;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: $z-feedback;
    padding: 4rem 1rem 1rem;
    color: rgb(var(--c-black));
    background: rgb(var(--c-selected));
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 300ms;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
