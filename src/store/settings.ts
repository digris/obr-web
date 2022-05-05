/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state", "getters"] }] */
import { useLocalStorage } from "@vueuse/core";

export interface Settings {
  maxBandwidth: number;
}

const maxBandwidth = useLocalStorage("settings/stream/maxBandwidth", 0);

const state: Settings = {
  // maxBandwidth: 0,
  // maxBandwidth: localStorage.getItem("settings/stream/maxBandwidth"),
  maxBandwidth: maxBandwidth.value,
};

const getters = {
  maxBandwidth: (state: Settings) => state.maxBandwidth,
};

const mutations = {
  SET_MAX_BANDWIDTH: (state: Settings, value: number) => {
    state.maxBandwidth = value;
  },
};

const actions = {
  setMaxBandwidth: async (context: any, value: number) => {
    maxBandwidth.value = value;
    context.commit("SET_MAX_BANDWIDTH", value);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
