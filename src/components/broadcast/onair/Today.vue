<script lang="ts">
import { defineComponent, onMounted } from 'vue';

import CloseButton from '@/components/ui/panel/CloseButton.vue';
import Program from '@/components/broadcast/program/Program.vue';

export default defineComponent({
  components: {
    CloseButton,
    Program,
  },
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
  <div
    class="today"
    v-if="isVisible"
  >
    <div
      class="title"
    >
      <CloseButton
        @click="close"
      />
      <span>
        Heute
      </span>
    </div>
    <div
      class="body"
    >
      <Program />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.today {
  position: fixed;
  top: 78px;
  z-index: 101;
  width: 100%;
  height: calc(100vh - 78px);
  max-height: calc(100vh - 78px);
  overflow-y: hidden;
  background: rgb(var(--c-white));
  .title {
    @include typo.x-large;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(var(--c-black))
  }
  .body {
    max-height: calc(100vh - 78px);
    overflow-y: auto;
    background: yellow;
    overscroll-behavior: contain;
    &::-webkit-scrollbar {
      display: none;
    }
  }
}
</style>
