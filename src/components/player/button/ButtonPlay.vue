<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import IconPlay from "@/components/ui/icon/IconPlay.vue";
import IconPlaying from "@/components/ui/icon/IconPlaying.vue";
import IconBuffering from "@/components/ui/icon/IconBuffering.vue";
import IconPause from "@/components/ui/icon/IconPause.vue";
import Circle from "./Circle.vue";

export default defineComponent({
  components: {
    Circle,
    IconPlay,
    IconPlaying,
    IconPause,
  },
  props: {
    size: {
      type: Number,
      default: 48,
    },
    color: {
      type: String,
      default: "rgb(var(--c-fg))",
    },
    // backgroundColor:
    // default is transparent, using 'color' if isActive
    backgroundColor: {
      type: String,
      default: null,
    },
    hoverBackgroundColor: {
      type: String,
      default: null,
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
    outlined: {
      type: Boolean,
      default: true,
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
    return {
      icon,
      isHover,
      onHover,
      onHout,
      handleClick,
    };
  },
});
</script>

<template>
  <Circle
    @mouseover="onHover"
    @mouseleave="onHout"
    @click.prevent="handleClick"
    :size="size"
    :outlined="outlined"
    :outline-width="outlineWidth"
    :outline-opacity="outlineOpacity"
    :disabled="disabled"
    :active="isActive"
    :background-color="backgroundColor"
    :hover-background-color="isPlaying ? 'rgb(var(--c-fg))' : hoverBackgroundColor"
    :class="{
      'is-playing': isPlaying,
      'is-buffering': isBuffering,
      'is-hover': isHover,
      'has-shadow': shadowed,
    }"
    :style="{
      height: `${size}px`,
      width: `${size}px`,
    }"
  >
    <component :is="icon" :size="size" :color="color" />
  </Circle>
</template>
<style lang="scss" scoped>
.circle-button {
  &.has-shadow {
    box-shadow: 0 0 8px rgb(0 0 0 / 50%);
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 100ms;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
