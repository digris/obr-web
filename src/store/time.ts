/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import { DateTime } from "luxon";

export interface State {
  stationTime: DateTime;
  playheadTime: DateTime | null;
}

const state: State = {
  stationTime: DateTime.now(),
  playheadTime: null,
};

const getters = {
  stationTime: (state: State) => state.stationTime,
  playheadTime: (state: State) => state.playheadTime,
  // eslint-disable-next-line arrow-body-style
  time: (state: State) => {
    return state.playheadTime ? state.playheadTime : state.stationTime;
  },
  // eslint-disable-next-line @typescript-eslint/no-shadow
  offset: (state: State, getters: any) => {
    return Math.floor((getters.stationTime - getters.time) / 1000);
  },
};

const mutations = {
  SET_STATION_TIME: (state: State, stationTime: DateTime) => {
    state.stationTime = stationTime;
  },
  SET_PLAYHEAD_TIME: (state: State, playheadTime: DateTime) => {
    state.playheadTime = playheadTime;
  },
};

const actions = {
  setStationTime: async (context: any, stationTime: DateTime) => {
    context.commit("SET_STATION_TIME", stationTime);
  },
  setPlayheadTime: async (context: any, playheadTime: DateTime) => {
    context.commit("SET_PLAYHEAD_TIME", playheadTime);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
