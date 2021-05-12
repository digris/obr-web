/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getRating, postRating } from '@/api/rating';

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
  // @ts-ignore
  SET_RATINGS: (state, ratings) => {
    state.ratings = ratings;
  },
};

const actions = {
  // @ts-ignore
  loadRating: async (context, key: string) => {
    const rating = await getRating(key);
    context.commit('SET_RATING', { key, rating });
  },
  updateObjectRatings: async (context: any, objects: Array<any>) => {
    objects.forEach((obj) => {
      const key = `${obj.ct}:${obj.uid}`;
      if (!context.getters.ratingByKey(key)) {
        const rating = {
          value: obj.userRating,
        };
        context.commit('SET_RATING', { key, rating });
      }
    });
  },
  updateRating: async (context: any, vote: object) => {
    // @ts-ignore
    const { key, ...rating } = vote;
    // context.commit('SET_RATING', { key, rating });
    const newRating = await postRating(key, rating);
    context.commit('SET_RATING', { key, rating: newRating });
  },
  clearRatings: async (context: any) => {
    context.commit('SET_RATINGS', []);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
