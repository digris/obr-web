import type { Schedule, Media } from "@/typings/api";
import { defineStore } from "pinia";
import { DateTime } from "luxon";
import { useTimeStore } from "@/stores/time";
import { getSchedule } from "@/api/broadcast";

export type AnnotatedSchedule = Schedule & {
  dtStart: DateTime;
  dtEnd: DateTime;
};

interface State {
  schedule: Array<AnnotatedSchedule>;
}

export const useScheduleStore = defineStore("schedule", {
  state: (): State => ({
    schedule: [],
  }),
  getters: {
    time(): DateTime {
      const { time } = useTimeStore();
      return time;
    },
    current(state: State): AnnotatedSchedule | null {
      const item = state.schedule.find(
        // (s: AnnotatedSchedule) => s.dtStart <= this.time && s.dtEnd > this.time
        // NOTE: check possible implications
        (s: AnnotatedSchedule) => s.dtStart <= this.time
      );
      return item ? item : null;
    },
    currentMedia(): Media | null {
      return this.current?.media ?? null;
    },
    items(state: State): Array<AnnotatedSchedule> {
      if (this.current?.dtStart) {
        const dtStart = this.current?.dtStart;
        return state.schedule.filter((s) => s.dtStart <= dtStart);
      }
      return [];
    },
    past(state: State): Array<AnnotatedSchedule> {
      if (this.current?.dtStart) {
        const dtStart = this.current?.dtStart;
        return state.schedule.filter((s) => s.dtStart < dtStart);
      }
      return [];
    },
    upcoming(state: State): Array<AnnotatedSchedule> {
      if (this.current?.dtStart) {
        const dtStart = this.current?.dtStart;
        return state.schedule.filter((s) => s.dtStart > dtStart);
      }
      return [];
    },
    next(): AnnotatedSchedule | null {
      if (this.upcoming.length) {
        return this.upcoming[this.upcoming.length - 1];
      }
      return null;
    },
    // items(): Array<AnnotatedSchedule | null> {
    //   return [this.next, this.current, ...this.past];
    // },
  },
  actions: {
    async loadSchedule(): Promise<void> {
      const params = {
        secondsAhead: 120 * 60,
        secondsBack: 120 * 60,
      };
      const result = await getSchedule(params);
      this.schedule = result.map((el: Schedule): AnnotatedSchedule => {
        return {
          ...el,
          dtStart: DateTime.fromISO(el.timeStart),
          dtEnd: DateTime.fromISO(el.timeEnd),
        };
      });
    },
  },
});
