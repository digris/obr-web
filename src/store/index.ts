import { createStore } from "vuex";

import account from "./account";
import catalog from "./catalog";
import broadcast from "./broadcast";
import program from "./program";
import notification from "./notification";

export default createStore({
  modules: {
    account,
    catalog,
    broadcast,
    program,
    notification,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
