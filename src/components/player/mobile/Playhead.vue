<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { refAutoReset, useElementSize } from "@vueuse/core";
import { round } from "lodash-es";

import Duration from "@/components/ui/time/Duration.vue";
import { usePlayerState } from "@/proto/composables/player";

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
    const { media, isOndemand, relPosition, currentTime, duration } = usePlayerState();
    const rootEl = ref<HTMLElement | null>(null);
    const { width: rootWidth } = useElementSize(rootEl);

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

    const seekPosition = ref(0);
    const isSeeking = refAutoReset(false, 500);

    const progress = computed(() => {
      const pos = isSeeking.value ? seekPosition.value / 100 : relPosition?.value ?? 0;
      return round(rootWidth.value * pos - rangeStart.value, 1);
    });

    const timeLeft = computed(() => {
      if (!currentTime.value) {
        return duration.value;
      }
      return duration.value - currentTime.value - media.value?.cueOut;
    });

    const rangeMin = computed(() => {
      return cueIn.value * 100;
    });

    const rangeMax = computed(() => {
      return (1 - cueOut.value) * 100;
    });

    const rangeStart = computed(() => {
      return round(cueIn.value * rootWidth.value, 0);
    });

    const rangeEnd = computed(() => {
      return round((1 - cueOut.value) * rootWidth.value, 0);
    });

    const rangeWidth = computed(() => {
      return round(rangeEnd.value - rangeStart.value, 0);
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

    // NOTE: just for debugging: visualize the fades
    const fadeInWidth = computed(() => {
      if (media.value?.fadeIn && duration.value) {
        return round((media.value?.fadeIn / duration.value) * rootWidth.value, 0);
      }
      return 0;
    });

    const fadeOutWidth = computed(() => {
      if (media.value?.fadeOut && duration.value) {
        return round((media.value?.fadeOut / duration.value) * rootWidth.value, 0);
      }
      return 0;
    });

    return {
      rootEl,
      isOndemand,
      isSeeking,
      onInput,
      onChange,
      currentTime,
      timeLeft,
      duration,
      cueIn,
      cueOut,
      relPosition,
      seekPosition,
      progress,
      rangeMin,
      rangeMax,
      rangeStart,
      rangeEnd,
      rangeWidth,
      // debug
      fadeInWidth,
      fadeOutWidth,
    };
  },
});
</script>

<template>
  <div v-if="isOndemand" ref="rootEl" class="playhead">
    <div class="track" />
    <div v-if="cueIn" class="cue cue--in" :style="{ left: `${rangeStart}px` }" />
    <div v-if="cueOut" class="cue cue--out" :style="{ left: `${rangeEnd}px` }" />
    <!-- NOTE: debug output -->
    <div
      v-if="fadeInWidth"
      class="fade fade--in"
      :style="{ left: `${rangeStart}px`, width: `${fadeInWidth}px` }"
    />
    <div
      v-if="fadeOutWidth"
      class="fade fade--out"
      :style="{ left: `${rangeEnd - fadeOutWidth}px`, width: `${fadeOutWidth}px` }"
    />
    <div
      v-if="duration"
      class="range"
      :style="{
        width: `${rangeWidth}px`,
        left: `${rangeStart}px`,
      }"
    >
      <input
        @change="onChange"
        @input.self="onInput"
        type="range"
        :min="rangeMin"
        :max="rangeMax"
        step="0.1"
        :class="{ 'is-seeking': isSeeking }"
      />
      <div
        class="progress"
        :style="{
          width: `${progress}px`,
        }"
        :class="{ 'is-seeking': isSeeking }"
      />
      <transition name="thumb">
        <div
          v-if="isSeeking"
          class="thumb"
          :style="{
            left: `${progress - 10}px`,
          }"
          :class="{ 'is-seeking': isSeeking }"
        />
      </transition>
    </div>
    <Duration v-if="currentTime" class="time time--current" :seconds="currentTime" />
    <div class="time time--total">-<Duration v-if="timeLeft" :seconds="timeLeft" /></div>
  </div>
  <div v-else class="playhead-placeholder" />
  <!--
  <pre class="debug" v-text="{ fadeInWidth, fadeOutWidth }" />
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
    background: rgb(var(--c-fg) / 20%);
  }

  .cue {
    top: 12px;
    position: absolute;
    height: 9px;
    width: 1px;
    background: rgb(var(--c-fg));
  }

  .fade {
    top: 22px;
    position: absolute;
    height: 1px;
    background: rgb(var(--c-fg));
  }

  .range {
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
      background: rgb(var(--c-fg) / 100%);
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
      box-shadow: 0 0 4px rgb(var(--c-fg) / 50%);

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
