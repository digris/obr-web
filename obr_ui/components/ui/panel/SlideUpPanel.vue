<script lang="ts">
import { computed, defineComponent, watch } from "vue";
import { useRoute } from "vue-router";
import { useEventListener } from "@vueuse/core";

export default defineComponent({
  components: {},
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
      close,
      hasFooter,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" @click="close" class="mask" />
  </transition>
  <transition name="slide">
    <div v-if="isVisible" class="slide-up-panel">
      <div class="container">
        <div class="slide-up-panel__content">
          <div v-if="title" class="slide-up-panel__content__title">
            <div v-text="title" />
          </div>
          <div class="slide-up-panel__content__body">
            <slot name="default" />
          </div>
          <div v-if="hasFooter" class="slide-up-panel__footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/container";

.mask {
  top: 0;
  position: fixed;
  height: 100%;
  width: 100%;
  z-index: 20;
  left: 0;
  background: rgb(var(--c-black) / 80%);

  @include responsive.bp-medium {
    background: unset;
  }
}

.slide-up-panel {
  position: fixed;
  width: 100%;
  min-height: 100px;
  bottom: 72px; // player height (desktop)
  max-height: calc(100% - 72px);
  left: 0;
  z-index: 45;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  font-weight: 500;
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

  .container {
    @include container.small;

    display: flex;
    flex-direction: column;
    padding-bottom: 1rem;
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
      @include typo.large;
      @include typo.bold;

      padding: 1.5rem 0;
    }
  }
}

// mask transition
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

// queue panel transition
.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms, opacity 200ms;
}

.slide-enter-from {
  transform: translate(0, 100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translate(0, 200%);
}
</style>
