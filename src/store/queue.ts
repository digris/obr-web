/* eslint no-shadow: ["error", { "allow": ["state"] }] */

export interface Queue {
  mode: string,
  media: Array<object>,
}

export interface State {
  media: Array<object>,
  currentIndex: Number,
}

const state: State = {
  media: [],
  currentIndex: -1,
};

const getters = {
  media: (state:any) => state.media,
  numMedia: (state:any) => state.media.length,
  // @ts-ignore
  totalDuration: (state:any) => state.media.reduce((a:number, m:object) => a + m.duration, 0),
  currentIndex: (state:any) => state.currentIndex,
  previousIndex: (state:any) => {
    if (state.media[state.currentIndex - 1]) {
      return state.currentIndex - 1;
    }
    return null;
  },
  nextIndex: (state:any) => {
    if (state.media[state.currentIndex + 1]) {
      return state.currentIndex + 1;
    }
    return null;
  },
  currentMedia: (state:any) => state.media[state.currentIndex],
};

const mutations = {
  REPLACE_MEDIA: (state:any, media:Array<object>) => {
    state.media = media;
    state.currentIndex = (media.length) ? 0 : -1;
  },
  SET_CURRENT_INDEX: (state:any, index: Number) => {
    state.currentIndex = index;
  },
};

const actions = {
  updateQueue: async (context:any, queue: Queue) => {
    const { media, mode } = queue;
    if (mode === 'replace') {
      context.commit('REPLACE_MEDIA', media);
    }
  },
  setIndex: async (context:any, index: Number) => {
    context.commit('SET_CURRENT_INDEX', index);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
