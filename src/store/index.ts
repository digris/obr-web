import { createStore } from "vuex";

import account from "./account";
import catalog from "./catalog";
import program from "./program";
import notification from "./notification";

export default createStore({
  modules: {
    account,
    catalog,
    program,
    notification,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
