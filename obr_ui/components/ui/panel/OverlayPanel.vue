<script lang="ts">
import { computed, defineComponent, watch } from "vue";
import { useRoute } from "vue-router";
import { useEventListener } from "@vueuse/core";

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
    useEventListener(document, "keydown", (e) => {
      if (e.code === "Escape") {
        close();
      }
    });
    const route = useRoute();
    watch(() => route.path, close);
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
    <div v-if="isVisible" class="overlay-panel">
      <div class="header">
        <CloseButton @click.prevent="close" />
      </div>
      <div class="container">
        <div class="overlay-panel__content">
          <div v-if="title" class="overlay-panel__content__title">
            <div v-text="title" />
          </div>
          <div class="overlay-panel__content__body">
            <slot name="default" />
          </div>
        </div>
        <div v-if="hasFooter" class="overlay-panel__footer">
          <slot name="footer" />
        </div>
        <div v-if="hasSuccess" class="overlay-panel__success">
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

.overlay-panel {
  top: var(--sa-t);
  position: fixed;
  height: 100%;
  width: 100%;
  left: 0;
  z-index: 45;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: rgb(var(--c-dark) / 100%);
  font-weight: 500;
  background: rgb(var(--c-light) / 100%);
  overflow-y: auto;
  overscroll-behavior: auto contain;

  @include responsive.bp-medium {
    box-shadow: 0 -4px 8px 4px rgb(0 0 0 / 10%);
    border-top-left-radius: 28px;
    border-top-right-radius: 28px;
  }

  &::-webkit-scrollbar {
    display: none;
  }

  .header {
    @include container.small;

    top: 0;
    position: sticky;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-top: 1rem;
    padding-bottom: 1rem;
    background: rgb(var(--c-light) / 100%);
    z-index: 50;

    @include responsive.bp-medium {
      height: 60px;
      min-height: 60px;
    }
  }

  .container {
    @include container.small;

    display: flex;
    flex-direction: column;
    height: 100%;
    padding-bottom: 4rem;
    min-height: calc(100vh - 79px);
  }

  @include responsive.bp-medium {
    max-width: unset;
  }

  &__header {
    position: fixed;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 78px;
    margin-top: 0;
  }

  &__content {
    flex-grow: 1;

    &__title {
      @include typo.x-large;
      @include typo.bold;

      padding: 0.5rem 0 1.5rem;
    }
  }
}

.fade-enter-active {
  transition: transform 200ms ease-in-out;
}

.fade-leave-active {
  transition: transform 200ms ease-in-out;
}

.fade-enter-from {
  opacity: 0;

  @include responsive.bp-medium {
    opacity: unset;
    transform: translate(0, 100%);
  }
}

.fade-leave-to {
  opacity: 0;

  @include responsive.bp-medium {
    opacity: unset;
    transform: translate(0, 100%);
  }
}
</style>
