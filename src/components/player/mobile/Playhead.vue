<script lang="ts">
import { computed, defineComponent } from "vue";
import { DateTime } from "luxon";
import { usePlayerState, usePlayerControls } from "@/composables/player";

import Duration from "@/components/ui/time/Duration.vue";
import Progress from "./PlayheadProgress.vue";

export default defineComponent({
  components: {
    Duration,
    Progress,
  },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const { isLive, isPlaying, isBuffering, duration, currentTime, relPosition } = usePlayerState();
    const { seek } = usePlayerControls();
    const strLiveTime = computed(() => {
      if (!isLive.value) {
        return "";
      }
      const dt = DateTime.fromJSDate(currentTime.value);
      return dt.toLocaleString({
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    });
    return {
      isLive,
      isPlaying,
      isBuffering,
      currentTime,
      duration,
      relPosition,
      strLiveTime,
      seek,
    };
  },
});
</script>

<template>
  <div
    class="playhead"
    :class="{
      'is-disabled': disabled,
    }"
  >
    <div class="progress">
      <div class="time time--current">
        <span v-if="isLive" v-text="strLiveTime" />
        <Duration v-else :seconds="currentTime" />
      </div>
      <div class="time time--total">
        <Duration v-if="duration" :seconds="duration" />
      </div>
      <Progress
        :is-live="isLive"
        :is-playing="isPlaying"
        :is-buffering="isBuffering"
        :rel-position="relPosition"
        @seek="seek"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.playhead {
  display: grid;
  width: 100%;
  min-height: 48px;
  .progress,
  .time {
    display: flex;
    align-items: center;
    transition: opacity 100ms;
  }
  .progress {
    position: relative;
    margin: 0 1rem;
    .time {
      @include typo.small;
      @include typo.bold;
      position: absolute;
      top: 0;
      display: flex;
      justify-content: center;
      padding: 0 1px;
      &--current {
        left: 0;
      }
      &--total {
        @include typo.dim;
        right: 0;
      }
    }
  }
  &.is-disabled {
    pointer-events: none;
    .progress {
      .time {
        opacity: 1;
      }
      .playhead-progress {
        opacity: 0.4;
      }
    }
  }
}
</style>
