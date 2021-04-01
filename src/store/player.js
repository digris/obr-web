/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

const state = {
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playhead: {},
  playerState: null,
};

const getters = {
  playerState: (state) => state.playerState,
};

const mutations = {
  SET_PLAYER_STATE: (state, { playerState }) => {
    state.playerState = playerState;
  },
};

const actions = {
  updatePlayerState: async (context, { playerState }) => {
    context.commit('SET_PLAYER_STATE', { playerState });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
