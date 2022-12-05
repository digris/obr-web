<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { refAutoReset, useElementSize } from "@vueuse/core";
import { round } from "lodash-es";

import Duration from "@/components/ui/time/Duration.vue";
import { usePlayerState } from "@/composables/player";

const mapRange = (
  input: number,
  from: readonly [number, number],
  to: readonly [number, number]
) => {
  return ((input - from[0]) / (from[1] - from[0])) * (to[1] - to[0]) + to[0];
};

export default defineComponent({
  components: {
    Duration,
  },
  props: {
    canSeek: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["seek"],
  setup(props, { emit }) {
    const { media, isOndemand, relPosition: progress, absPosition, duration } = usePlayerState();
    const root = ref<HTMLElement | null>(null);
    const inputEl = ref<HTMLElement | null>(null);
    const hasFocus = ref(false);
    const { width: inputWidth } = useElementSize(inputEl);

    const cueIn = computed(() => {
      if (media.value?.cueIn && duration.value) {
        return round(media.value?.cueIn / duration.value, 3);
      }
      return 0;
    });

    const cueOut = computed(() => {
      if (media.value?.cueOut && duration.value) {
        return round(media.value?.cueOut / duration.value, 3);
      }
      return 0;
    });

    const rangeMin = computed(() => {
      return cueIn.value * 100;
    });

    const rangeMax = computed(() => {
      return (1 - cueIn.value) * 100;
    });

    const rangeWidth = computed(() => {
      return (1 - cueIn.value - cueOut.value) * 100;
    });

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
      // const toDomain = isSeeking.value ? [10, width - 10] : [0, width];
      return mapRange(inputValue.value, [rangeMin.value, rangeMax.value], [0, width]);
    });

    const playheadJustify = computed(() => {
      if (cueIn.value && cueOut.value) {
        return "center";
      } else if (cueIn.value) {
        return "end";
      } else if (cueOut.value) {
        return "start";
      }
      return "center";
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
      playheadJustify,
      absPosition,
      duration,
      cueIn,
      cueOut,
      rangeMin,
      rangeMax,
      rangeWidth,
    };
  },
});
</script>

<template>
  <div v-if="isOndemand" ref="root" class="playhead" :style="{ justifyContent: playheadJustify }">
    <div class="track" />
    <div v-if="cueIn" class="cue cue--in" :style="{ left: `${cueIn * 100}%` }" />
    <div v-if="cueOut" class="cue cue--out" :style="{ right: `${cueOut * 100}%` }" />
    <div
      v-if="duration"
      class="seek-container"
      :style="{
        width: `${rangeWidth}%`,
      }"
    >
      <input
        ref="inputEl"
        @change="onChange"
        @input.self="onInput"
        type="range"
        :min="rangeMin"
        :max="rangeMax"
        step="0.1"
        :value="inputValue"
        :class="{ 'is-seeking': isSeeking }"
      />
      <div
        class="progress"
        :style="{
          // width: `${inputValue}%`,
          width: `${paddedInputValue}px`,
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
    <Duration v-if="absPosition" class="time time--current" :seconds="absPosition" />
    <Duration v-if="duration" class="time time--total" :seconds="duration" />
  </div>
  <div v-else class="playhead-placeholder" />
  <!--
  <pre
    class="debug"
    v-text="{
      duration,
      cueIn,
      cueOut,
      rangeMin,
      rangeMax,
      inputWidth,
    }"
  />
  -->
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.playhead {
  display: flex;
  position: relative;
  min-height: 32px;

  .track {
    top: 14px;
    position: absolute;
    height: 4px;
    width: 100%;
    pointer-events: none;
    background: rgb(var(--c-fg) 0.2);
  }

  .cue {
    top: 12px;
    position: absolute;
    height: 9px;
    width: 2px;
    background: rgb(var(--c-fg));
  }

  .seek-container {
    position: relative;
    width: 100%;

    input[type="range"] {
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
        appearance: none;
        opacity: 0;
        margin-top: 12px;
        height: 20px;
        width: 20px;
      }
    }

    .progress {
      top: 14px;
      position: absolute;
      height: 4px;
      width: 1%;
      pointer-events: none;
      background: rgb(var(--c-fg) 1);
      transition: width 100ms linear;

      &.is-seeking {
        transition-duration: 1ms;
      }
    }

    .thumb {
      top: 6px;
      position: absolute;
      height: 20px;
      width: 20px;
      background: rgb(var(--c-bg) 1);
      border-radius: 10px;
      pointer-events: none;
      transition: left 100ms linear;
      box-shadow: 0 0 4px rgb(var(--c-fg) 0.5);

      &.is-seeking {
        transition-duration: 1ms;
      }

      &::after {
        top: 6px;
        position: absolute;
        height: 8px;
        width: 8px;
        content: "";
        background: rgb(var(--c-fg));
        left: 6px;
        border-radius: 4px;
      }
    }
  }

  .time {
    @include typo.small;

    top: -10px;
    position: absolute;
    pointer-events: none;

    &--current {
      left: 0;
    }

    &--total {
      right: 0;
    }
  }
}

.debug {
  @include typo.small;
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
