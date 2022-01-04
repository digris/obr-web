<script lang="ts">
import {
  defineComponent,
  onMounted,
} from 'vue';

import CloseButton from './CloseButton.vue';

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
      default: '',
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
  <transition
    name="fade"
  >
    <div
      v-if="isVisible"
      class="overlay-panel"
    >
      <div
        class="container"
      >
        <div
          class="overlay-panel__header"
        >
          <CloseButton
            @click.prevent="close"
          />
        </div>
        <div
          v-if="title"
          class="overlay-panel__title"
        >
          <div
            v-text="title"
          />
        </div>
        <div
          class="overlay-panel__body"
        >
          <slot
            name="default"
          />
        </div>
        <div
          class="overlay-panel__success"
        >
          <slot
            name="success"
          />
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.overlay-panel {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 29;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100%;
  //overflow: hidden;
  color: rgb(var(--c-black));
  font-weight: 500;
  background: rgb(var(--c-white));

  .container {
    @include container.small;
    //height: 100%;
  }

  @include responsive.bp-small {
    max-width: unset;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 72px;
    margin-top: 0;
    border-bottom: 1px solid rgb(var(--c-gray-100));
  }
  &__title {
    @include typo.x-large;
    @include typo.bold;
    padding: 0.5rem 0 1.5rem;
  }
  &__body {
    //flex-grow: 1;
    //padding-top: 2rem;
    //padding: 0 4rem 1rem;
    //max-height: calc(100% - 172px);
    //overflow-y: auto;
    background: transparent;
  }
  &__footer {
    //padding: 1rem 4rem;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 300ms;
}
.fade-enter-from {
  opacity: 0;
}
.fade-leave-to {
  opacity: 0;
}
</style>
