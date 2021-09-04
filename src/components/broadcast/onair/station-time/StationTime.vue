<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import { playStream } from '@/player/stream';

import ToggleTimeshiftButton from './ToggleTimeshiftButton.vue';
import ResetTimeshiftButton from './ResetTimeshiftButton.vue';

const TIMESHIFT_OFFSET = 30;

const zeroPad = (n:number) => {
  return n > 9 ? `${n}` : `0${n}`;
};

export default defineComponent({
  components: {
    ToggleTimeshiftButton,
    ResetTimeshiftButton,
  },
  emits: [
    'releaseFocus',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const time = computed(() => {
      return store.getters['time/time'];
    });
    const hour = computed(() => {
      return zeroPad(time.value.hour);
    });
    const minute = computed(() => {
      return zeroPad(time.value.minute);
    });
    const second = computed(() => {
      return zeroPad(time.value.second);
    });
    const offset = computed(() => {
      return store.getters['time/offset'];
    });
    const isTimeshifted = computed(() => {
      return offset.value > TIMESHIFT_OFFSET;
    });
    const releaseFocus = () => {
      emit('releaseFocus');
    };
    const resetTimeshift = () => {
      playStream();
    };
    return {
      time,
      hour,
      minute,
      second,
      isTimeshifted,
      offset,
      releaseFocus,
      resetTimeshift,
    };
  },
});
</script>

<template>
  <div
    class="station-time"
  >
    <div
      class="actions"
    >
      <ToggleTimeshiftButton />
    </div>
    <div
      class="container"
    >
      <div
        v-if="(!isTimeshifted)"
        class="time"
        @click="releaseFocus"
      >
        <span
          class="hour"
        >{{ hour }}</span>
        <span
          class="separator separator--minute"
        >:</span>
        <span
          class="minute"
        >{{ minute }}</span>
        <!--
        <span
          class="separator separator--second"
        >:</span>
        <span
          class="second"
        >{{ second }}</span>
        -->
      </div>
      <div
        v-if="isTimeshifted"
        class="time-shift"
      >
        <div
          class="offset"
          :title="offset"
        >
          &ndash; {{ offset }} Sec.
        </div>
        <div>
          <ResetTimeshiftButton
            @click="resetTimeshift"
          />
        </div>
      </div>
    </div>
    <div
      class="actions"
    >
      <ToggleTimeshiftButton />
    </div>
  </div>
</template>
<style lang="scss">
@keyframes pulsate {
  50% {
    opacity: 0;
  }
}
</style>
<style lang="scss" scoped>
@use "sass:math";
@use "@/style/base/live-color";
@use "@/style/elements/container";
$width: 200px;
$height: 48px;
.station-time {
  //@include container.default;
  display: grid;
  grid-template-columns: 48px 1fr 48px;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem 0;
}
.container {
  @include live-color.fg;
  position: relative;
  display: inline-flex;
  grid-column-start: 2;
  align-items: center;
  justify-content: center;
  min-width: $width;
  height: 78px;
  user-select: none;
  .time {
    display: grid;
    flex-grow: 1;
    //grid-template-columns: 64px 32px 64px 32px 64px;
    grid-template-columns: 64px 32px 64px;
    align-items: center;
    justify-content: center;

    //padding-left: $height;
    > span {
      justify-self: center;
    }
    .hour,
    .minute,
    .second {
      font-weight: 600;
      font-size: 64px;
    }
    .separator {
      font-size: 32px;
      animation: pulsate 2s linear infinite;
    }
  }
  .time-shift {
    @include live-color.fg;
    display: grid;
    grid-template-columns: 36px 1fr 36px;
    align-items: center;
    justify-content: center;
    min-width: $width;
    height: 3rem;
    border: 3px solid transparent;
    border-color: inherit;
    border-radius: math.div($height, 2);
    .offset {
      grid-column-start: 2;
      justify-self: center;
    }
  }
}
</style>
