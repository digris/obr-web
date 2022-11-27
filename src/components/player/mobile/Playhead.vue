<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { refAutoReset, useElementSize } from "@vueuse/core";
import { usePlayerState } from "@/composables/player";

const mapRange = (
  input: number,
  from: readonly [number, number],
  to: readonly [number, number]
) => {
  return ((input - from[0]) / (from[1] - from[0])) * (to[1] - to[0]) + to[0];
};

export default defineComponent({
  props: {
    canSeek: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["seek"],
  setup(props, { emit }) {
    const { isOndemand, relPosition: progress } = usePlayerState();
    const root = ref<HTMLElement | null>(null);
    const inputEl = ref<HTMLElement | null>(null);
    const hasFocus = ref(false);
    const { width: inputWidth } = useElementSize(inputEl);

    const seekPosition = ref(0);
    const isSeeking = refAutoReset(false, 500);

    const inputValue = computed(() => {
      if (isSeeking.value) {
        return seekPosition.value;
      } else {
        return progress.value ? progress.value * 100 : 0;
      }
    });

    const paddedInputValue = computed(() => {
      const width = inputWidth.value;
      const toDomain = isSeeking.value ? [10, width - 10] : [0, width];
      return mapRange(inputValue.value, [0, 100], toDomain);
    });

    const onInput = (e: Event) => {
      const value = Number((e.target as HTMLInputElement).value);
      isSeeking.value = true;
      seekPosition.value = value;
    };
    const onChange = (e: Event) => {
      const value = Number((e.target as HTMLInputElement).value);
      emit("seek", value * 0.01);
    };
    return {
      root,
      isOndemand,
      inputEl,
      hasFocus,
      isSeeking,
      inputValue,
      paddedInputValue,
      inputWidth,
      onInput,
      onChange,
    };
  },
});
</script>

<template>
  <div v-if="isOndemand" ref="root" class="playhead">
    <input
      ref="inputEl"
      @change="onChange"
      @input.self="onInput"
      type="range"
      min="0"
      max="100"
      step="0.1"
      :value="inputValue"
      :class="{ 'is-seeking': isSeeking }"
    />
    <div class="track" />
    <div
      class="progress"
      :style="{
        width: `${inputValue}%`,
      }"
      :class="{ 'is-seeking': isSeeking }"
    />
    <transition name="thumb">
      <div
        v-if="isSeeking"
        class="thumb"
        :style="{
          left: `${paddedInputValue - 10}px`,
        }"
        :class="{ 'is-seeking': isSeeking }"
      />
    </transition>
  </div>
  <div v-else class="playhead-placeholder" />
</template>

<style lang="scss" scoped>
//.playhead-placeholder {
//  height: 100%;
//}
.playhead {
  position: relative;
  min-height: 32px;
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    background: transparent;
    height: 32px;
    width: 100%;
    &:focus {
      outline: none;
    }
    // track
    &::-webkit-slider-runnable-track {
      height: 32px;
    }
    // thumb (used as handler only)
    &::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      opacity: 0;
      margin-top: 12px;
      height: 20px;
      width: 20px;
    }
  }
  .track,
  .progress {
    width: 100%;
    position: absolute;
    //left: 2px; // why??
    pointer-events: none;
  }
  .track {
    background: rgba(var(--c-fg), 0.2);
    height: 4px;
    top: 14px;
  }
  .progress {
    background: rgba(var(--c-fg), 1);
    height: 4px;
    top: 14px;
    width: 1%;
    transition: width 100ms linear;
    &.is-seeking {
      transition-duration: 1ms;
    }
  }
  .thumb {
    background: rgba(var(--c-bg), 1);
    //border: 1px solid rgba(var(--c-fg), 1);
    border-radius: 10px;
    width: 20px;
    height: 20px;
    position: absolute;
    pointer-events: none;
    top: 6px;
    transition: left 100ms linear;
    box-shadow: 0 0 4px rgba(var(--c-fg), 0.5);
    &.is-seeking {
      transition-duration: 1ms;
    }
    &:after {
      content: "";
      width: 8px;
      height: 8px;
      background: rgb(var(--c-fg));
      position: absolute;
      top: 6px;
      left: 6px;
      border-radius: 4px;
    }
  }
}

.thumb-enter-active,
.thumb-leave-active {
  transition: transform 200ms;
  transform: scale(1);
}
.thumb-enter-from {
  transform: scale(0);
}
.thumb-leave-to {
  transform: scale(0);
}
</style>
