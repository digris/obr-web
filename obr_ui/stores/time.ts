import { computed, ref } from "vue";
import { useIntervalFn } from "@vueuse/core";
import { DateTime } from "luxon";
import { defineStore } from "pinia";

import settings from "@/settings";

const INTERVAL = 1000;
const FIXED_LATENCY = settings.STREAM_LATENCY;

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
