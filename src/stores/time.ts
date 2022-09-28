import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useIntervalFn } from "@vueuse/core";
import { DateTime } from "luxon";

const INTERVAL = 200;
const FIXED_LATENCY = 27;

export const useTimeStore = defineStore("time", () => {
  const now = ref(DateTime.now());
  const streamLatency = ref(0);
  const latency = computed(() => {
    return FIXED_LATENCY + streamLatency.value;
  });
  const time = computed(() => {
    return now.value.minus({ seconds: latency.value });
  });
  const { pause, resume } = useIntervalFn(() => {
    now.value = DateTime.now();
  }, INTERVAL);
  return {
    time,
    latency,
    pause,
    resume,
  };
});
