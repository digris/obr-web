/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state", "getters"] }] */

export interface Queue {
  media: Array<object>,
  scope: Array<string>,
}

export interface State {
  media: Array<object>,
  currentIndex: number,
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
  currentMedia: (state: State) => state.media[state.currentIndex],
  // currentScope is implemented in store/player.ts
  // currentScope: (state: State, getters: any) => {
  //   return getters.currentMedia ? getters.currentMedia.scope : [];
  // },
};

const mutations = {
  SET_CURRENT_INDEX: (state:any, index: number) => {
    state.currentIndex = index;
  },
  REMOVE_INDEX: (state:any, index: number) => {
    state.media.splice(index, 1);
  },
  REPLACE_MEDIA: (state:any, queue: Queue) => {
    const { media, scope } = queue;
    const mappedMedia = media.map((el) => {
      return { ...el, scope };
    });
    state.media = mappedMedia;
    state.currentIndex = (media.length) ? 0 : -1;
  },
};

const actions = {
  setIndex: async (context:any, index: number) => {
    context.commit('SET_CURRENT_INDEX', index);
  },
  removeIndex: async (context:any, index: number) => {
    context.commit('REMOVE_INDEX', index);
  },
  replaceQueue: async (context:any, queue: Queue) => {
    context.commit('REPLACE_MEDIA', queue);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
