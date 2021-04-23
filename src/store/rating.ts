/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getRating } from '@/api/rating';

const state = {
  ratings: [],
};

const getters = {
  // @ts-ignore
  ratings: (state) => state.ratings,
  // @ts-ignore
  ratingByKey: (state) => (key: string) => state.ratings[key] || null,
};

const mutations = {
  // @ts-ignore
  SET_RATING: (state, { key, rating }) => {
    // @ts-ignore
    state.ratings[key] = rating;
  },
};

const actions = {
  // @ts-ignore
  loadRating: async (context, key: string) => {
    const rating = await getRating(key);
    context.commit('SET_RATING', { key, rating });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
