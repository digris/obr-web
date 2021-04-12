/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

const state = {
  encodingFormat: 'dash',
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
  encodingFormat: (state) => state.encodingFormat,
  // @ts-ignore
  playerState: (state) => state.playerState,
  // @ts-ignore
  currentMedia: (state) => state.currentMedia,
};

const mutations = {
  // @ts-ignore
  SET_ENCODING_FORMAT: (state, encodingFormat) => {
    state.encodingFormat = encodingFormat;
  },
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
  updateEncodingFormat: async (context, encodingFormat) => {
    context.commit('SET_ENCODING_FORMAT', encodingFormat);
  },
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
