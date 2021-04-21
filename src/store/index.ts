import { createStore } from 'vuex';

import time from './time';
import account from './account';
import ui from './ui';
import catalog from './catalog';
import player from './player';
import schedule from './schedule';

export default createStore({
  // namespaced: true,
  modules: {
    time,
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
