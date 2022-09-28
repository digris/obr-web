import { storeToRefs } from "pinia";
import { useIntervalFn } from "@vueuse/core";
import { useScheduleStore } from "@/stores/schedule";
import store from "@/store";
import { watch } from "vue";

class Schedule {
  constructor() {
    const interval = 61 * 1000;
    const { loadSchedule } = useScheduleStore();

    useIntervalFn(
      async () => {
        await store.dispatch("schedule/loadSchedule");
        await loadSchedule();
      },
      interval,
      { immediateCallback: true }
    );

    const { current: currentItem } = storeToRefs(useScheduleStore());
    watch(
      () => currentItem.value,
      (value) => {
        console.debug('currentItem', value);
      },
    );

    // eslint-disable-next-line arrow-body-style
    store.watch(
      (state: any, getters: any) => {
        return getters["time/time"];
      },
      (time) => {
        const current = store.getters["schedule/current"];
        if (current && current.timeStart <= time && current.timeEnd > time) {
          return;
        }
        const schedule = store.getters["schedule/schedule"];
        if (!schedule.length) {
          return;
        }
        const newCurrent = schedule.find((s: any) => s.timeStart <= time && s.timeEnd > time);
        if (newCurrent) {
          Schedule.updateCurrent(newCurrent);
        }
      }
    );
  }

  static async updateCurrent(item: any) {
    const current = store.getters["schedule/current"];
    if (current && current.key === item.key) {
      return;
    }
    await store.dispatch("schedule/updateCurrent", item);
  }
}

export default function () {
  return new Schedule();
}
