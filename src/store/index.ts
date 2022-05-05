import { createStore } from "vuex";

import time from "./time";
import account from "./account";
import settings from "./settings";
import ui from "./ui";
import rating from "./rating";
import catalog from "./catalog";
import broadcast from "./broadcast";
import player from "./player";
import queue from "./queue";
import program from "./program";
import schedule from "./schedule";
import notification from "./notification";

export default createStore({
  modules: {
    time,
    account,
    settings,
    ui,
    rating,
    catalog,
    broadcast,
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
