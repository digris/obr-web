<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import type { PropType } from "vue";
import { useIconSize } from "@/composables/icon";
import { getContrastColor } from "@/utils/color";
import IconPlay from "@/components/ui/icon/IconPlay.vue";
import IconPlayQueued from "@/components/ui/icon/IconPlayQueued.vue";
import IconPlaying from "@/components/ui/icon/IconPlaying.vue";
import IconBuffering from "@/components/ui/icon/IconBuffering.vue";
import IconPause from "@/components/ui/icon/IconPause.vue";

export default defineComponent({
  components: {},
  props: {
    scale: {
      type: Number,
      default: 1,
    },
    baseColor: {
      type: Array as PropType<Array<number>>,
      default: () => [10, 10, 10],
    },
    activeColor: {
      type: Array as PropType<Array<number>>,
      default: () => [10, 10, 10],
    },
    fillColor: {
      type: Array as PropType<Array<number>>,
      default: () => [10, 10, 10],
    },
    isPlaying: {
      type: Boolean,
      default: false,
    },
    isBuffering: {
      type: Boolean,
      default: false,
    },
    isActive: {
      type: Boolean,
      default: false,
    },
    inQueue: {
      type: Boolean,
      default: false,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
    filled: {
      type: Boolean,
      default: false,
    },
    outlineWidth: {
      type: Number,
      default: 1,
    },
    outlineOpacity: {
      type: Number,
      default: 0.15,
    },
    shadowed: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["play", "pause"],
  setup(props, { emit }) {
    const { iconSize } = useIconSize(props.scale);
    const isHover = ref(false);
    const icon = computed(() => {
      if (props.isBuffering) {
        return IconBuffering;
      }
      if (props.isPlaying && isHover.value) {
        return IconPause;
      }
      if (props.isPlaying) {
        return IconPlaying;
      }
      if (props.inQueue) {
        return IconPlayQueued;
      }
      return IconPlay;
    });
    const action = computed(() => {
      if (props.isBuffering || props.isPlaying) {
        return "pause";
      }
      return "play";
    });
    const handleClick = () => {
      emit(action.value);
    };
    const onHover = () => {
      isHover.value = true;
    };
    const onHout = () => {
      isHover.value = false;
    };
    const fgColor = computed(() => {
      if (props.isActive) {
        return getContrastColor(props.activeColor);
      }
      return props.baseColor;
    });
    const bgColor = computed(() => {
      if (props.isActive) {
        return props.activeColor;
      }
      return props.fillColor;
    });
    const isOutlined = computed(() => {
      return props.outlined;
    });
    const isFilled = computed(() => {
      if (props.isActive) {
        return true;
      }
      return props.filled;
    });
    const hoverBgOpacity = computed(() => {
      if (isFilled.value) {
        return 0.8;
      }
      return 0.1;
    });
    return {
      icon,
      iconSize,
      isHover,
      onHover,
      onHout,
      handleClick,
      //
      fgColor,
      bgColor,
      isOutlined,
      isFilled,
      hoverBgOpacity,
    };
  },
});
</script>

<template>
  <div
    class="button-play"
    :class="{
      'is-outlined': isOutlined,
      'is-filled': isFilled,
      'is-hover': isHover,
    }"
    :style="{
      '--size': `${iconSize}px`,
      '--c-fg': fgColor.join(','),
      '--c-bg': bgColor.join(','),
      '--hover-bg-opacity': hoverBgOpacity,
      '--outline-width': `${outlineWidth}px`,
      '--outline-opacity': outlineOpacity,
    }"
  >
    <component :is="icon" :scale="scale" />
    <div v-if="isOutlined" class="outline" />
    <div
      @click.prevent="handleClick"
      @mouseover.stop="onHover"
      @mouseout.stop="onHout"
      class="trigger-area"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
.button-play {
  position: relative;
  display: inline-grid;
  align-items: center;
  justify-content: center;
  border-radius: calc(var(--size) / 2);
  cursor: pointer;
  transition: background-color 750ms;
  .outline {
    position: absolute;
    top: -1px;
    left: -1px;
    width: calc(100% + 2px);
    height: calc(100% + 2px);
    border: var(--outline-width) solid rgba(var(--c-fg), var(--outline-opacity));
    border-radius: calc(var(--size) / 2);
  }
  &.is-filled {
    background: rgb(var(--c-bg));
  }
  @include responsive.on-hover {
    transition: background-color 200ms;
    background: rgba(var(--c-bg), var(--hover-bg-opacity));
  }
}
.trigger-area {
  background: transparent;
  position: absolute;
  width: var(--size);
  height: var(--size);
  border-radius: calc(var(--size) / 2);
}
</style>
