/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { ActionContext } from 'vuex';

export interface State {
  colors: {
   bg: string,
   fg: string,
  }
}

const state: State = {
  colors: {
    bg: '0, 0, 0',
    fg: '250, 250, 250',
  },
};

const getters = {
  colors: (state: State) => state.colors,
};

const mutations = {
  // @ts-ignore
  SET_COLORS: (state: State, { colors }) => {
    state.colors = colors;
  },
};

const actions = {
  // @ts-ignore
  setPrimaryColor: async (context, color: string) => {
    const colors = {
      bg: color,
      fg: '#eeeeee',
    };
    context.commit('SET_COLORS', { colors });
    console.debug('setPrimaryColor', color);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
