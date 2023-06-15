import { DateTime } from "luxon";
import { defineStore } from "pinia";

import { getSchedule } from "@/api/broadcast";
import { useTimeStore } from "@/stores/time";
import type { Schedule, ScheduleMedia } from "@/typings/api";

export type AnnotatedSchedule = Schedule & {
  dtStart: DateTime;
  dtEnd: DateTime;
};

export type AnnotatedScheduleMedia = ScheduleMedia & {
  cueIn?: number;
  cueOut?: number;
  fadeIn?: number;
  fadeOut?: number;
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
    currentMedia(): AnnotatedScheduleMedia | null{
      return this.current?.media ?? null;
    },
    nextMedia(): AnnotatedScheduleMedia | null{
      return this.next?.media ?? null;
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
    async setSchedule(data: Array<Schedule>): Promise<void> {
      // used by app-bridge in app-mode
      this.schedule = data.map((el: Schedule): AnnotatedSchedule => {
        return {
          ...el,
          dtStart: DateTime.fromISO(el.timeStart),
          dtEnd: DateTime.fromISO(el.timeEnd),
        };
      });
    },
  },
});
