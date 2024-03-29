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
  },
  emits: ["close"],
  setup(props, { emit, slots }) {
    const hasAside = computed(() => !!slots.aside);
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
      hasAside,
      close,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" @click.prevent="close" class="mask" />
  </transition>
  <transition name="fade">
    <div v-if="isVisible && hasAside" class="aside">
      <slot name="aside" />
    </div>
  </transition>
  <transition name="slide">
    <div v-if="isVisible" class="side-panel">
      <div class="side-panel__header">
        <div class="slot">
          <slot name="header" />
        </div>
        <div class="close">
          <CloseButton @click.prevent="close" />
        </div>
      </div>
      <div class="side-panel__body">
        <slot name="default" />
      </div>
      <div class="side-panel__footer">
        <slot name="footer" />
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.mask {
  inset: 0;
  position: fixed;
  z-index: 111;
  background: rgb(0 0 0 / 90%);
  backdrop-filter: grayscale(70%) brightness(80%);

  @include responsive.bp-medium {
    background: unset;
    backdrop-filter: unset;
  }
}

.side-panel {
  top: var(--sa-t);

  // padding-top: var(--sa-t);
  padding-bottom: calc(var(--sa-b) + var(--sa-t));
  position: fixed;
  height: 100%;
  width: 100%;
  right: 0;
  z-index: 112;
  display: flex;
  flex-direction: column;
  max-width: 50vw;
  min-width: 50vw;
  color: rgb(var(--c-dark) / 100%);
  font-weight: 500;
  background: rgb(var(--c-light) / 100%);
  transition: background 400ms;

  @include responsive.bp-medium {
    max-width: unset;
    box-shadow: 0 -4px 8px 4px rgb(0 0 0 / 10%);
    border-top-left-radius: 28px;
    border-top-right-radius: 28px;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 75px;
    margin: 0 1.5rem 0.5rem;
    border-bottom: 1px solid rgb(var(--c-dark) / 20%);

    .slot {
      flex-grow: 1;
    }

    @include responsive.bp-medium {
      height: 60px;
      margin: 0 0.5rem;

      .close {
        display: flex;
      }
    }
  }

  &__body {
    flex-grow: 1;
    padding: 0 1.5rem 1rem;
    overflow-y: auto;

    @include responsive.bp-medium {
      padding: 0 0.625rem 0.5rem;
    }
  }

  &__footer {
    margin: 0 1.5rem;
    padding: 1rem 0;
    border-top: 1px solid rgb(var(--c-dark) / 20%);

    @include responsive.bp-medium {
      margin: 0 0.625rem;
      padding: 0.5rem 0;
    }
  }
}

.aside {
  top: 0;
  position: fixed;
  height: 100%;
  width: 50vw;
  left: 0;
  z-index: 111;
  display: flex;
  flex-direction: column;
  padding-top: calc(75px + 0.5rem);
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  color: rgb(var(--c-light) / 100%);

  @include responsive.bp-medium {
    display: none;
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
  transition: transform 200ms ease-out;
}

.slide-enter-from {
  transform: translate(100%, 0);

  @include responsive.bp-medium {
    transform: translate(0, 100%);
  }
}

.slide-leave-to {
  transform: translate(100%, 0);

  @include responsive.bp-medium {
    transform: translate(0, 100%);
  }
}
</style>
