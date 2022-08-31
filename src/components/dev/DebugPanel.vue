<script lang="ts">
import { computed, defineComponent } from "vue";

import { useTime } from "@/composables/time";

const DEBUG = false;

export default defineComponent({
  setup() {
    const { time, stationTime, playheadTime } = useTime();
    const debugVars = computed(() => {
      return {
        time: time.value,
        stationTime: stationTime.value,
        playheadTime: playheadTime.value,
      };
    });
    return {
      visible: DEBUG,
      debugVars,
    };
  },
});
</script>

<template>
  <div v-if="visible" class="debug-panel">
    <pre v-text="debugVars" />
  </div>
</template>

<style lang="scss" scoped>
.debug-panel {
  position: fixed;
  bottom: 80px;
  left: 10px;
  padding: 1rem;
  font-weight: 300;
  font-size: 0.8rem;
  color: #ffffff;
  background: #000;
}
</style>
