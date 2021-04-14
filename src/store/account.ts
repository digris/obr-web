/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { login, getCurrentUser } from '@/api/account';

export interface State {
  currentUser: object | null,
}
export interface Credentials {
  email: string,
  password: string,
}

const state: State = {
  currentUser: null,
};

const getters = {
  currentUser: (state: State) => state.currentUser,
};

const mutations = {
  SET_USER: (state: State, user: object | null) => {
    state.currentUser = user;
  },
};

const actions = {
  loginUser: async (context: any, credentials: Credentials) => {
    const { email, password } = credentials;
    let user: object | null;
    try {
      user = await login(email, password);
    } catch (err) {
      console.warn(err);
      user = null;
    }
    context.commit('SET_USER', user);
  },
  getUser: async (context: any) => {
    let user: object | null;
    try {
      user = await getCurrentUser();
    } catch (err) {
      console.warn(err);
      user = null;
    }
    console.debug(user);
    context.commit('SET_USER', user);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
