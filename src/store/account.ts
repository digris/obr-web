/* eslint @typescript-eslint/no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import {
  login,
  logout,
  loginByToken,
  loginBySignedEmail,
  getUser,
} from '@/api/account';

export interface State {
  user: any | null,
  subscription: any | null,
  settings: any | null,
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
  user: null,
  subscription: null,
  settings: null,
};

const getters = {
  user: (state: State) => state.user,
  subscription: (state: State) => state.subscription,
  settings: (state: State) => state.settings,
};

const mutations = {
  SET_USER: (state: State, user: any | null) => {
    // @ts-ignore
    const { subscription, settings, ...bareUser } = { ...user };
    state.user = Object.keys(bareUser).length ? bareUser : null;
    state.subscription = subscription;
    state.settings = settings;
  },
  /*
  SET_SUBSCRIPTION: (state: State, subscription: any | null) => {
    state.subscription = subscription;
  },
  SET_SETTINGS: (state: State, settings: any | null) => {
    state.settings = settings;
  },
  */
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
      user = await getUser();
    } catch (err) {
      console.warn(err);
      user = null;
    }
    context.commit('SET_USER', user);

    /*
    const { subscription, settings, ...user } = { ...fullUser };
    context.commit('SET_USER', Object.keys(user).length ? user : null);
    context.commit('SET_SUBSCRIPTION', subscription);
    context.commit('SET_SETTINGS', settings);
    */
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
