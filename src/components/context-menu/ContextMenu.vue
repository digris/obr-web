<script type="ts">
import {
  defineComponent,
  ref,
  computed,
  onMounted,
} from 'vue';

import { onClickOutside } from '@vueuse/core';
import { useIconSize } from "@/composables/icon";
import eventBus from '@/eventBus';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconContext from '@/components/ui/icon/IconContext.vue';
import ObjectActions from './ObjectActions.vue';
import ListActions from './ListActions.vue';
import { useDevice } from '@/composables/device';

export default defineComponent({
  props: {
    obj: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    list: {
      type: Object,
      required: false,
      default: () => ({
        filter: {},
        ordering: [],
      }),
    },
    iconScale: {
      type: Number,
      default: 1,
    },
  },
  components: {
    CircleButton,
    IconContext,
    ObjectActions,
    ListActions,
  },
  setup(props) {
    const root = ref(null);
    const menu = ref(null);
    const menuPosition = ref('bottom');
    const { defaultIconSize } = useIconSize();
    const iconSize = computed(() => {
      return defaultIconSize.value * props.iconScale;
    });
    const { isDesktop } = useDevice();
    const isVisible = ref(false);
    const isObj = computed(() => Object.keys(props.obj).length);
    const show = (e) => {
      const { pageY } = e;
      const height = window.innerHeight;
      if ((height - pageY) < 240) {
        menuPosition.value = 'top';
      } else {
        menuPosition.value = 'bottom';
      }
      isVisible.value = true;
    };
    const hide = () => {
      isVisible.value = false;
    };
    const transitionName = computed(() => {
      return isDesktop.value ? 'fade' : 'slide';
    });
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
    onClickOutside(menu, () => hide());
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
      menu,
      menuPosition,
      iconSize,
      isVisible,
      isObj,
      show,
      hide,
      transitionName,
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
    <div class="context-menu__icon" @click.prevent="show">
      <CircleButton :scale="iconScale">
        <IconContext :scale="iconScale" />
      </CircleButton>
    </div>
    <transition :name="transitionName">
      <div class="menu-container" v-if="isVisible" :class="`position-${menuPosition}`">
        <div class="menu" ref="menu" @mouseleave="onMenuMouseleave" @mouseenter="onMenuMouseenter">
          <ObjectActions v-if="isObj" :obj="obj" @close="hide" />
          <ListActions v-else :filter="list.filter" :ordering="list.ordering" @close="hide" />
        </div>
      </div>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
.context-menu {
  position: relative;
  &__icon {
    width: var(--icon-size);
    height: var(--icon-size);
  }
  .menu-container {
    position: absolute;
    right: 0;
    .menu {
      position: absolute;
      right: 0;
      z-index: 50;
      min-width: 300px;
      background: rgba(0, 0, 0, 1);
      border-radius: 4px;
      box-shadow: 0 0 10px rgb(0 0 0 / 30%);
      .actions {
        background: rgba(255, 255, 255, 1);
      }
    }
    &.position-top {
      bottom: 0;
      .menu {
        bottom: 0;
      }
    }
    &.position-bottom {
      top: 0;
      .menu {
        top: 0;
      }
    }
    @include responsive.bp-medium {
      position: fixed;
      top: 0;
      left: 0;
      z-index: 120; // use 100 to move behind player
      display: flex;
      align-items: flex-end;
      width: 100%;
      height: 100%;
      //background: rgba(var(--c-black), 0.8);
      background: rgba(0, 0, 0, 0.8);
      .menu {
        position: unset;
        width: 100%;
        border-radius: unset;
        box-shadow: unset;
        padding-bottom: 120px;
        background: rgb(0, 0, 0);
      }
    }
  }
}

// desktop
.fade-enter-active,
.fade-leave-active {
  opacity: 1;
  transition: opacity 100ms linear;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

// mobile
.slide-enter-active,
.slide-leave-active {
  opacity: 1;
  //transition: transform 200ms, opacity 200ms;
  transition: transform 400ms, opacity 100ms linear;
  .menu {
    transition: transform 300ms;
    transition-delay: 100ms;
  }
}
.slide-enter-from {
  opacity: 0;
  .menu {
    transform: translate(0, 100%);
  }
}
.slide-leave-to {
  opacity: 0;
  .menu {
    transform: translate(0, 100%);
  }
}
</style>
