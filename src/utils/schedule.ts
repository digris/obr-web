import { useIntervalFn } from "@vueuse/core";
import { useScheduleStore } from "@/stores/schedule";
// import store from "@/store";

class Schedule {
  constructor() {
    const interval = 61 * 1000;
    const { loadSchedule } = useScheduleStore();

    useIntervalFn(
      async () => {
        await loadSchedule();
      },
      interval,
      { immediateCallback: true }
    );
  }
}

export default function () {
  return new Schedule();
}
