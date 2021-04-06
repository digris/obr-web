import { createStore } from 'vuex';

import ui from './ui';
import catalog from './catalog';
import player from './player';

export default createStore({
  // namespaced: true,
  modules: {
    ui,
    catalog,
    player,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
