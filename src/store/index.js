import { createStore } from 'vuex';

import player from './player';

export default createStore({
  namespaced: true,
  modules: {
    player,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
