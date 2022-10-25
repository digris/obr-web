import { createStore } from "vuex";

import account from "./account";
import catalog from "./catalog";
import notification from "./notification";

export default createStore({
  modules: {
    account,
    catalog,
    notification,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
