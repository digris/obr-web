import { createStore } from 'vuex';

import account from './account';
import ui from './ui';
import catalog from './catalog';
import player from './player';
import schedule from './schedule';

export default createStore({
  // namespaced: true,
  modules: {
    account,
    ui,
    catalog,
    player,
    schedule,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
