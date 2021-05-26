/* eslint no-shadow: ["error", { "allow": ["state"] }] */

export interface Queue {
  mode: string,
  media: Array<object>,
}

export interface State {
  media: Array<object>,
}

const state: State = {
  media: [],
};

const getters = {
  media: (state:any) => state.media,
};

const mutations = {
  REPLACE_MEDIA: (state:any, media:Array<object>) => {
    state.media = media;
  },
};

const actions = {
  updateQueue: async (context:any, queue: Queue) => {
    const { media, mode } = queue;
    console.debug('updateQueue', media, mode);
    context.commit('REPLACE_MEDIA', media);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
