/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state", "getters"] }] */
import { DateTime } from 'luxon';

const state = {
  configuration: {},
  bufferInfo: {},
  currentState: null,
  playheadTime: null,
  playerState: null,
  isLive: false,
  media: null,
};

const getters = {
  playheadTime: (state: any) => state.playheadTime,
  playerState: (state: any) => state.playerState,
  isLive: (state: any) => state.isLive,
  media: (state: any) => state.media,
  playState: (state: any, getters: any) => {
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
  release: (state: any, getters: any) => {
    return getters.media?.releases?.length ? getters.media.releases[0] : null;
  },
  scope: (state: any, getters: any) => {
    return getters.media?.scope ?? [];
    // return (getters.media && getters.media.scope) ? getters.media.scope : [];
  },
  color: (state: any, getters: any) => {
    return getters.release?.image?.rgb ?? [0, 0, 0];
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
    state.media = media;
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
