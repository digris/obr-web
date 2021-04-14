import { createStore } from 'vuex';

import account from './account';
import ui from './ui';
import catalog from './catalog';
import player from './player';

export default createStore({
  // namespaced: true,
  modules: {
    account,
    ui,
    catalog,
    player,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
