<script lang="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';

const TIMESHIFT_OFFSET = 30;

export default {
  setup() {
    const store = useStore();
    const time = computed(() => {
      return store.getters['time/time'];
    });
    const formattedTime = computed(() => {
      console.debug(time);
      return time.value.toLocaleString(DateTime.TIME_24_WITH_SECONDS);
    });
    const offset = computed(() => {
      return store.getters['time/offset'];
    });
    const isTimeshifted = computed(() => {
      return offset.value > TIMESHIFT_OFFSET;
    });
    return {
      formattedTime,
      time,
      isTimeshifted,
      offset,
    };
  },
};
</script>

<template>
  <div
    class="container"
  >
    <div
      class="station-time"
    >
      <div
        class="time"
      >
        <span
          class="hour"
        >{{ time.hour }}</span>
        <span
          class="separator"
        >:</span>
        <span
          class="minute"
        >{{ time.minute }}</span>
        <span
          class="separator"
        >:</span>
        <span
          class="second"
        >{{ time.second }}</span>
      </div>
      <div
        v-if="isTimeshifted"
        class="time-shift"
        :class="{'is-active': isTimeshifted}"
      >
        <span
          :title="offset">
          TS
        </span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
@use "@/style/elements/container";
$width: 200px;
$height: 40px;
.container {
  @include container.default;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}
.station-time {
  @include live-color.fg;
  display: inline-flex;
  min-width: $width;
  height: $height;
  border: 2px solid transparent;
  border-color: inherit;
  .time {
    display: grid;
    flex-grow: 1;
    grid-template-columns: 20px 10px 20px 10px 20px;
    align-items: center;
    justify-content: center;
    //padding-left: $height;
    > span {
      justify-self: center;
    }
  }
  .time-shift {
    @include live-color.bg-inverse;
    @include live-color.fg-inverse;
    display: flex;
    align-items: center;
    justify-content: center;
    width: $height;
    opacity: 0;
    &.is-active {
      opacity: 1;
    }
  }
}
</style>
