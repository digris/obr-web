<script lang="ts">
import { storeToRefs } from "pinia";
import { computed, defineComponent } from "vue";

import { useTimeStore } from "@/stores/time";
import { zeroPad } from "@/utils/format";

export default defineComponent({
  setup() {
    const { time } = storeToRefs(useTimeStore());
    const hour = computed(() => {
      return zeroPad(time.value.hour);
    });
    const minute = computed(() => {
      return zeroPad(time.value.minute);
    });
    return {
      hour,
      minute,
    };
  },
});
</script>

<template>
  <div class="station-time">
    <span class="hour" v-text="hour" />
    <span class="separator separator--minute" v-text="`:`" />
    <span class="minute" v-text="minute" />
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
@use "@/style/base/live-color";

.station-time {
  display: grid;
  grid-template-columns: 1em 0.5em 1em;
  align-items: center;
  justify-content: center;
  font-size: 64px;
  transition: background-color 20ms, color 100ms, font-size 200ms;

  > span {
    justify-self: center;
  }

  .hour,
  .minute {
    font-weight: 600;
    font-size: 1em;
  }

  .separator {
    font-size: 0.5em;
    animation: pulsate 2s linear infinite;
  }
}
</style>
