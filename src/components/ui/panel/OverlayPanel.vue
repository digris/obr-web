<script lang="ts">
import { computed, defineComponent, watch } from "vue";
import { useEventListener } from "@vueuse/core";
import { useRoute } from "vue-router";

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
  position: fixed;
  top: 0;
  left: 0;
  z-index: 45;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
  color: rgb(var(--c-black));
  font-weight: 500;
  background: rgb(var(--c-white));
  //background: rgb(0, 0, 0);
  overflow-y: auto;
  &::-webkit-scrollbar {
    display: none;
  }
  overscroll-behavior: auto contain;

  .header {
    @include container.small;
    position: sticky;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-top: 1rem;
    padding-bottom: 1rem;
    background: rgb(var(--c-white));
    z-index: 50;
    @include responsive.bp-medium {
      height: 60px;
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
  /*
  &__footer {
    padding: 1rem 0;
    background: red;
  }
  */
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
