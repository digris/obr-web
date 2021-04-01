/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

const state = {
  colors: {
    bg: '0, 0, 0',
    fg: '250, 250, 250',
  },
};

const getters = {
  colors: (state) => state.colors,
};

const mutations = {
  SET_COLORS: (state, { colors }) => {
    state.colors = colors;
  },
};

const actions = {
  setPrimaryColor: async (context, color) => {
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
