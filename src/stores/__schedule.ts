import { defineStore } from "pinia";
import { DateTime } from "luxon";
import type { Schedule } from "@/typings/api";
import { useTime } from "@/composables/time";
import { getSchedule } from "@/api/broadcast";

export type AnnotatedSchedule = Schedule & {
  dtStart: DateTime;
  dtEnd: DateTime;
};

interface State {
  schedule: Array<AnnotatedSchedule>;
  // current: AnnotatedSchedule | null;
}

export const useScheduleStore = defineStore("schedule", {
  state: (): State => ({
    schedule: [],
    // current: null,
  }),
  getters: {
    time(): DateTime {
      const { time } = useTime();
      return time.value;
    },
    current(state: State) {
      return state.schedule.find(
        (s: AnnotatedSchedule) => s.dtStart <= this.time && s.dtEnd > this.time
      );
    },
    currentMedia(state: State) {
      return state.current?.media ?? null;
    },
    past(state: State) {
      if (!state.current) {
        return [];
      }
      return state.schedule.filter((s) => s.dtStart < state.current.dtStart);
    },
    upcoming(state: State) {
      if (!state.current) {
        return [];
      }
      return state.schedule.filter((s) => s.dtStart > state.current.dtStart);
    },
    next(): AnnotatedSchedule | null {
      if (!this.upcoming.length) {
        return null;
      }
      return this.upcoming[this.upcoming.length - 1];
    },
  },
  actions: {
    async loadSchedule(): Promise<void> {
      const params = {
        secondsAhead: 120 * 60,
        secondsBack: 120 * 60,
      };
      console.debug("stores/schedule: loadSchedule", params);
      const result = await getSchedule(params);
      const parsedSchedule: Array<AnnotatedSchedule> = [];
      result.forEach((el: Schedule) => {
        const s: AnnotatedSchedule = {
          ...el,
          dtStart: DateTime.fromISO(el.timeStart),
          dtEnd: DateTime.fromISO(el.timeEnd),
        };
        parsedSchedule.push(s);
      });
      console.debug("parsedSchedule", parsedSchedule);

      this.schedule = parsedSchedule;

      // this.schedule = result.forEach((el: Schedule): AnnotatedSchedule => {
      //   return {
      //     ...el,
      //     dtStart: DateTime.fromISO(el.timeStart),
      //     dtEnd: DateTime.fromISO(el.timeEnd),
      //   };
      // });
    },
    updateCurrent(current: AnnotatedSchedule) {
      console.debug("stores/schedule: updateCurrent", current);
      this.current = current;
    },
  },
});
