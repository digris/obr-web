<script lang="ts">
import { defineComponent, onMounted } from "vue";

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
  setup(props, { emit }) {
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
      close,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" class="mask" />
  </transition>
  <transition name="slide">
    <div v-if="isVisible" class="side-panel">
      <div class="side-panel__header">
        <CloseButton @click.prevent="close" />
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
@use "@/style/abstracts/responsive";
.mask {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  background: rgba(var(--c-black), 0.9);
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
  font-weight: 500;
  background: rgb(var(--c-white));

  @include responsive.bp-small {
    max-width: unset;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 75px;
    margin: 0 4rem 1rem;
    border-bottom: 1px solid rgb(var(--c-gray-200));
    @include responsive.bp-small {
      margin: 0 1rem 1rem;
    }
  }
  &__body {
    flex-grow: 1;
    padding: 0 4rem 1rem;
    @include responsive.bp-small {
      padding: 0 1rem 1rem;
    }
  }
  &__footer {
    padding: 1rem 4rem;
    @include responsive.bp-small {
      padding: 0 1rem 1rem;
    }
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
