/* eslint no-shadow: ["error", { "allow": ["state"] }] */
import { DateTime } from 'luxon';

const state = {
  encodingFormat: 'dash',
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playheadTime: null,
  playerState: null,
  currentMedia: null,
};

const getters = {
  encodingFormat: (state:any) => state.encodingFormat,
  playheadTime: (state:any) => state.playheadTime,
  playerState: (state:any) => state.playerState,
  currentMedia: (state:any) => state.currentMedia,
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

  SET_CURRENT_MEDIA: (state:any, media:object) => {
    state.currentMedia = media;
  },
};

// @ts-ignore
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
