/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
// @ts-ignore
import { DateTime } from "luxon";
import { getSchedule } from "@/api/broadcast";

export interface State {
  schedule: Array<any>;
  current: Object | null;
}

const state: State = {
  schedule: [],
  current: null,
};

const getters = {
  schedule: (state: State) => state.schedule,
  current: (state: State) => state.current,
  currentMedia: (state: State) => {
    // @ts-ignore
    return state.current ? state.current.media : null;
  },
  past: (state: State) => {
    if (!state.current) {
      return [];
    }
    // @ts-ignore
    return state.schedule.filter((s) => s.timeStart < state.current.timeStart);
  },
  upcoming: (state: State) => {
    if (!state.current) {
      return [];
    }
    // @ts-ignore
    return state.schedule.filter((s) => s.timeStart > state.current.timeStart);
  },
  next: (state: State) => {
    if (!state.current) {
      return null;
    }
    const upcoming = getters.upcoming(state);
    return upcoming.length ? upcoming[upcoming.length - 1] : null;
  },
};

const mutations = {
  SET_SCHEDULE: (state: State, schedule: Array<any>) => {
    const parsedSchedule: Array<any> = [];
    schedule.forEach((el) => {
      const s = { ...el };
      s.timeStart = DateTime.fromISO(s.timeStart);
      s.timeEnd = DateTime.fromISO(s.timeEnd);
      parsedSchedule.push(s);
    });
    state.schedule = parsedSchedule;
  },
  SET_CURRENT: (state: State, current: Object) => {
    state.current = current;
  },
};

const actions = {
  loadSchedule: async (context: any) => {
    const params = {
      secondsAhead: 120 * 60,
      secondsBack: 120 * 60,
    };
    // NOTE: not sure if this should go here. so just for now...
    const isInitial = !context.getters.schedule.length;
    if (isInitial) {
      params.secondsBack = 120 * 60;
    }

    const schedule = await getSchedule(params);
    // console.table(schedule);
    context.commit("SET_SCHEDULE", schedule);
  },
  updateCurrent: async (context: any, current: Object) => {
    context.commit("SET_CURRENT", current);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
