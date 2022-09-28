import { createStore } from "vuex";

import time from "./time";
import account from "./account";
import catalog from "./catalog";
import broadcast from "./broadcast";
import queue from "./queue";
import program from "./program";
import schedule from "./schedule";
import notification from "./notification";

export default createStore({
  modules: {
    time,
    account,
    catalog,
    broadcast,
    queue,
    program,
    schedule,
    notification,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
