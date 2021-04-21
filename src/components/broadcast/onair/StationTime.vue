<script lang="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';

export default {
  setup() {
    const store = useStore();
    const stationTime = computed(() => {
      const dt = store.getters['time/stationTime'];
      return dt.toLocaleString(DateTime.TIME_24_WITH_SECONDS);
    });
    const playheadTime = computed(() => {
      const dt = store.getters['player/playheadTime'];
      if (dt) {
        return dt.toLocaleString(DateTime.TIME_24_WITH_SECONDS);
      }
      return null;
    });
    return {
      stationTime,
      playheadTime,
    };
  },
};
</script>

<template>
  <div
    class="station-time"
  >
    <div>
      <span>{{ stationTime }}</span>
      <span
        v-if="playheadTime"
        class="playhead-time"
      >{{ playheadTime }}</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.station-time {
  @include container.default;
  padding: 2rem 0;
  font-size: 120%;
  text-align: center;
  .playhead-time {
    padding-left: 1rem;
  }
}
</style>
