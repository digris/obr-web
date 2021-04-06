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
  // @ts-ignore
  playerState: (state) => state.playerState,
};

const mutations = {
  // @ts-ignore
  SET_PLAYER_STATE: (state, { playerState }) => {
    state.playerState = playerState;
  },
};

const actions = {
  // @ts-ignore
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
