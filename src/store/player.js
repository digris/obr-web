/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

const state = {
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playhead: {},
};

const getters = {
  configuration: (state) => state.configuration,
  bufferInfo: (state) => state.bufferInfo,
  currentState: (state) => state.currentState,
  playhead: (state) => state.playhead,
};

const mutations = {
  SET_CONFIGURATION: (state, { configuration }) => {
    state.configuration = configuration;
  },
  SET_BUFFER_INFO: (state, { bufferInfo }) => {
    state.bufferInfo = bufferInfo;
    if (bufferInfo.stateHistory.length) {
      // eslint-disable-next-line prefer-destructuring
      [state.currentState] = bufferInfo.stateHistory.slice(-1);
    } else {
      state.currentState = null;
    }
  },
  SET_PLAYHEAD: (state, { playhead }) => {
    state.playhead = playhead;
  },
};

const actions = {
  updateConfiguration: async (context, { configuration }) => {
    context.commit('SET_CONFIGURATION', { configuration });
  },
  updatePlayer: async (context, { player }) => {
    const playhead = player.getPlayheadTimeAsDate();
    const bufferInfo = player.getStats();
    context.commit('SET_BUFFER_INFO', { bufferInfo });
    context.commit('SET_PLAYHEAD', { playhead });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
