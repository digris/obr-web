<script type="ts">
import {
  computed,
  defineComponent,
  onMounted,
  ref,
} from 'vue';
import { onClickOutside } from '@vueuse/core';

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconContext from '@/components/ui/icon/IconContext.vue';
import { useDevice } from '@/composables/device';
import { useIconSize } from "@/composables/icon";
import eventBus from '@/eventBus';

import ListActions from './ListActions.vue';
import ObjectActions from './ObjectActions.vue';

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
    height: var(--icon-size);
    width: var(--icon-size);
  }

  .menu-container {
    position: absolute;
    right: 0;

    .menu {
      position: absolute;
      right: 0;
      z-index: 50;
      min-width: 300px;
      background: rgb(0 0 0 / 100%);
      border-radius: 4px;
      box-shadow: 0 0 10px rgb(0 0 0 / 30%);

      .actions {
        background: rgb(var(--c-light) / 100%);
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
      top: 0;
      position: fixed;
      height: 100%;
      width: 100%;
      left: 0;
      z-index: 120; // use 100 to move behind player
      display: flex;
      align-items: flex-end;
      background: rgb(0 0 0 / 80%);

      .menu {
        position: unset;
        width: 100%;
        border-radius: unset;
        box-shadow: unset;
        padding-bottom: 120px;
        background: rgb(0 0 0);
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
  transition: transform 400ms, opacity 100ms linear;
  /* stylelint-disable-next-line no-descending-specificity */
  .menu {
    transition: transform 300ms;
    transition-delay: 100ms;
  }
}

.slide-enter-from {
  opacity: 0;
  /* stylelint-disable-next-line no-descending-specificity */
  .menu {
    transform: translate(0, 100%);
  }
}

.slide-leave-to {
  opacity: 0;
  /* stylelint-disable-next-line no-descending-specificity */
  .menu {
    transform: translate(0, 100%);
  }
}
</style>
