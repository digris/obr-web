import { createStore } from "vuex";

import account from "./account";
import notification from "./notification";

export default createStore({
  modules: {
    account,
    notification,
  },
  mutations: {},
  actions: {},
  plugins: [],
});
