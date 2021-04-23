/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import { DateTime } from 'luxon';

const state = {
  encodingFormat: 'dash',
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playheadTime: null,
  playerState: null,
  // currentMedia: {
  //   name: 'Rock The Boat',
  //   artists: [
  //     {
  //       name: 'Inner Circle',
  //     },
  //   ],
  // },
  currentMedia: null,
};

const getters = {
  // @ts-ignore
  encodingFormat: (state) => state.encodingFormat,
  // @ts-ignore
  playheadTime: (state) => state.playheadTime,
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
    const { playheadTime, ...pState } = playerState;
    if (playheadTime) {
      state.playheadTime = DateTime.fromJSDate(playheadTime);
    } else {
      state.playheadTime = null;
    }
    state.playerState = pState;
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
