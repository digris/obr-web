/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import { DateTime } from 'luxon';

export interface State {
  stationTime: DateTime,
}

const state: State = {
  stationTime: DateTime.now(),
};

const getters = {
  stationTime: (state: State) => state.stationTime,
};

const mutations = {
  SET_STATION_TIME: (state: State, stationTime: DateTime) => {
    state.stationTime = stationTime;
  },
};

const actions = {
  setStationTime: async (context: any, stationTime: DateTime) => {
    context.commit('SET_STATION_TIME', stationTime);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
