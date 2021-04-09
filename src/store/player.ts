/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

const state = {
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playhead: {},
  playerState: null,
  currentMedia: {
    name: 'Rock The Boat',
    artists: [
      {
        name: 'Inner Circle',
      },
    ],
  },
};

const getters = {
  // @ts-ignore
  playerState: (state) => state.playerState,
  // @ts-ignore
  currentMedia: (state) => state.currentMedia,
};

const mutations = {
  // @ts-ignore
  SET_PLAYER_STATE: (state, { playerState }) => {
    state.playerState = playerState;
  },
  // @ts-ignore
  SET_CURRENT_MEDIA: (state, media) => {
    state.currentMedia = media;
  },
};

const actions = {
  // @ts-ignore
  updatePlayerState: async (context, { playerState }) => {
    context.commit('SET_PLAYER_STATE', { playerState });
  },
  // @ts-ignore
  updateCurrentMedia: async (context, media) => {
    context.commit('SET_CURRENT_MEDIA', media);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
