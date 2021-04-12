/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { ActionContext } from 'vuex';

export interface State {
  // primaryColor: Array<number>,
  title: string,
  primaryColor: [number, number, number],
}

const state: State = {
  title: 'open broadcast radio',
  primaryColor: [0, 0, 0],
};

const getters = {
  title: (state: State) => state.title,
  primaryColor: (state: State) => state.primaryColor,
};

const mutations = {
  SET_TITLE: (state: State, title: string) => {
    state.title = title;
  },
  SET_PRIMARY_COLOR: (state: State, color: [number, number, number]) => {
    state.primaryColor = color;
  },
};

const actions = {
  setTitle: async (context: any, title: string) => {
    context.commit('SET_TITLE', title);
  },
  setPrimaryColor: async (context: any, color: [number, number, number]) => {
    context.commit('SET_PRIMARY_COLOR', color);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
