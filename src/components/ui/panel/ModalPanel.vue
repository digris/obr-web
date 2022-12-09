<script lang="ts">
import { computed, defineComponent, onMounted } from "vue";

import CloseButton from "./CloseButton.vue";

export default defineComponent({
  components: {
    CloseButton,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "",
    },
  },
  emits: ["close"],
  setup(props, { slots, emit }) {
    const hasFooter = computed(() => !!slots.footer);
    const hasSuccess = computed(() => !!slots.success);
    const close = () => {
      emit("close");
    };
    onMounted(() => {
      document.addEventListener("keydown", (e) => {
        if (props.isVisible && e.code === "Escape") {
          close();
        }
      });
    });
    return {
      hasFooter,
      hasSuccess,
      close,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" class="modal-panel">
      <div class="container">
        <div class="modal-panel__header">
          <CloseButton @click.prevent="close" />
        </div>
        <div class="modal-panel__content">
          <div v-if="title" class="modal-panel__content__title">
            <div v-text="title" />
          </div>
          <div class="modal-panel__content__body">
            <slot name="default" />
          </div>
        </div>
        <div v-if="hasSuccess" class="modal-panel__success">
          <slot name="success" />
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";

.modal-panel {
  top: 0;
  position: fixed;
  height: 100%;
  width: 100%;
  left: 0;
  z-index: 29;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: rgb(var(--c-black) / 100%);
  font-weight: 500;
  background: rgb(var(--c-black) / 80%);

  .container {
    @include container.small;

    display: flex;
    flex-direction: column;
    padding-bottom: 1rem;
    background: rgb(var(--c-white) / 100%);
  }

  @include responsive.bp-medium {
    max-width: unset;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 78px;
    margin-top: 0;
  }

  &__content {
    flex-grow: 1;
    max-height: calc(100% - 72px);

    /* right padding for scrollbar */
    padding-right: 0.75rem;
    overflow-y: auto;
    overscroll-behavior: contain;

    &::-webkit-scrollbar {
      display: none;
    }

    &__title {
      @include typo.x-large;
      @include typo.bold;

      padding: 0.5rem 0 1.5rem;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 100ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>
