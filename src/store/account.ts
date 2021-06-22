/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import {
  login,
  logout,
  loginByToken,
  loginBySignedEmail,
  getCurrentUser,
} from '@/api/account';

export interface State {
  currentUser: any | null,
}
export interface Credentials {
  email: string,
  password: string,
}
export interface TokenCredentials {
  email: string,
  token: string,
}

const state: State = {
  currentUser: null,
};

const getters = {
  currentUser: (state: State) => state.currentUser,
};

const mutations = {
  SET_USER: (state: State, user: any | null) => {
    state.currentUser = user;
  },
};

const actions = {
  loginUser: async (context: any, credentials: Credentials) => {
    const { email, password } = credentials;
    try {
      const user = await login(email, password);
      context.commit('SET_USER', user);
    } catch (err) {
      console.warn(err);
      context.commit('SET_USER', null);
      throw err;
    }
  },
  logoutUser: async (context: any) => {
    try {
      await logout();
      context.commit('SET_USER', null);
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  loginUserByToken: async (context: any, credentials: TokenCredentials) => {
    const { email, token } = credentials;
    try {
      const user = await loginByToken(email, token);
      context.commit('SET_USER', user);
    } catch (err) {
      console.warn(err);
      context.commit('SET_USER', null);
      throw err;
    }
  },
  loginUserBySignedEmail: async (context: any, signedEmail: string) => {
    try {
      const user = await loginBySignedEmail(signedEmail);
      context.commit('SET_USER', user);
    } catch (err) {
      console.warn(err);
      context.commit('SET_USER', null);
      throw err;
    }
  },
  getUser: async (context: any) => {
    let user: any | null;
    try {
      user = await getCurrentUser();
    } catch (err) {
      console.warn(err);
      user = null;
    }
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
