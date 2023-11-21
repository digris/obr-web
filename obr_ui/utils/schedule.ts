import { useIntervalFn } from "@vueuse/core";

import { useDevice } from "@/composables/device";
import { useScheduleStore } from "@/stores/schedule";

class Schedule {
  constructor() {
    const interval = 61 * 1000;
    const { loadSchedule } = useScheduleStore();
    const { isWeb } = useDevice();

    if (isWeb) {
      useIntervalFn(
        async () => {
          await loadSchedule();
        },
        interval,
        { immediateCallback: true }
      );
    }
  }
}

export default function () {
  return new Schedule();
}
