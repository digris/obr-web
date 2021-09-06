/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state", "getters"] }] */
import { DateTime } from 'luxon';

const state = {
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playheadTime: null,
  playerState: null,
  isLive: false,
  currentMedia: null,
};

const getters = {
  playheadTime: (state: any) => state.playheadTime,
  playerState: (state: any) => state.playerState,
  playerPlayState: (state: any, getters: any) => {
    if (getters.playerState.isPlaying) {
      return 'playing';
    }
    if (getters.playerState.isPaused) {
      return 'paused';
    }
    if (getters.playerState.isBuffering) {
      return 'buffering';
    }
    return 'stopped';
  },
  isLive: (state: any) => state.isLive,
  currentMedia: (state: any) => state.currentMedia,
  currentScope: (state: any, getters: any) => {
    return getters.currentMedia ? getters.currentMedia.scope : [];
  },
};

const mutations = {
  // @ts-ignore
  SET_PLAYER_STATE: (state, playerState) => {
    const { playheadTime, ...pState } = playerState;
    if (playheadTime) {
      state.playheadTime = DateTime.fromJSDate(playheadTime);
    } else {
      state.playheadTime = null;
    }
    state.playerState = pState;
  },
  // @ts-ignore
  SET_ITEM: (state, item) => {
    // @ts-ignore
    const { isLive, media } = { ...item };
    state.isLive = isLive;
    state.currentMedia = media;
  },
};

const actions = {
  // @ts-ignore
  updatePlayerState: async (context, playerState) => {
    context.commit('SET_PLAYER_STATE', playerState);
  },
  // @ts-ignore
  updateCurrentItem: async (context, item) => {
    context.commit('SET_ITEM', item);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
