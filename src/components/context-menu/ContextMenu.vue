<script type="ts">
import {
  defineComponent,
  ref,
  computed,
  onMounted,
} from 'vue';

import { onClickOutside } from '@vueuse/core';

import eventBus from '@/eventBus';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconContext from '@/components/ui/icon/IconContext.vue';
import ObjectActions from './ObjectActions.vue';

export default defineComponent({
  props: {
    obj: {
      type: Object,
      required: true,
      default: () => {},
    },
    iconSize: {
      type: Number,
      default: 48,
    },
  },
  components: {
    CircleButton,
    IconContext,
    ObjectActions,
  },
  setup() {
    const root = ref(null);
    const isVisible = ref(false);
    const show = () => {
      eventBus.emit('contextMenu:show');
      isVisible.value = true;
    };
    const hide = () => {
      isVisible.value = false;
    };
    eventBus.on('contextMenu:show', () => {
      hide();
    });
    onMounted(() => {
      document.addEventListener('keydown', (e) => {
        if (isVisible.value && e.code === 'Escape') {
          hide();
        }
      });
      document.addEventListener('scroll', () => {
        if (isVisible.value) {
          hide();
        }
      });
    });
    onClickOutside(root, () => hide());
    const hideTimeout = ref(null);
    const onMenuMouseleave = () => {
      hideTimeout.value = setTimeout(() => {
        hide();
      }, 300);
    };
    const onMenuMouseenter = () => {
      clearTimeout(hideTimeout.value);
    };
    const actions = computed(() => {
      return [];
    });
    return {
      root,
      isVisible,
      show,
      hide,
      onMenuMouseleave,
      onMenuMouseenter,
      actions,
    };
  },
});
</script>

<template>
  <div
    ref="root"
    class="context-menu"
    :style="{
      '--icon-size': `${iconSize}px`,
    }"
  >
    <div
      class="context-menu__icon"
      @click.prevent="show"
    >
      <CircleButton
        :size="iconSize"
        :outlined="(false)"
      >
        <IconContext
          :size="iconSize"
        />
      </CircleButton>
    </div>
    <transition
      name="fade"
    >
      <div
        class="context-menu__menu"
        v-if="isVisible"
        @mouseleave="onMenuMouseleave"
        @mouseenter="onMenuMouseenter"
      >
        <ObjectActions
          :obj="obj"
          @close="hide"
        />
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
.context-menu {
  position: relative;
  &__icon {
    width: 48px;
    height: 48px;
  }
  &__menu {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 50;
    min-width: 300px;
    background: rgba(255, 255, 255, 1.0);
    border-radius: 4px;
    box-shadow: 0 0 10px rgb(0 0 0 / 30%);
  }
}
.fade-enter-active,
.fade-leave-active,
{
  opacity: 1;
  transition: opacity 100ms linear;
}

.fade-enter,
.fade-leave-to
{
  opacity: 0;
}
</style>
