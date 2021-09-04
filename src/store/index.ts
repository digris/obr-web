import { createStore } from 'vuex';

import time from './time';
import account from './account';
import ui from './ui';
import rating from './rating';
import catalog from './catalog';
import player from './player';
import queue from './queue';
import program from './program';
import schedule from './schedule';
import notification from './notification';

export default createStore({
  // namespaced: true,
  modules: {
    time,
    account,
    ui,
    rating,
    catalog,
    player,
    queue,
    program,
    schedule,
    notification,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
