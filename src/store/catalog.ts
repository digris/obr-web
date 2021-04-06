/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */

import { getArtist } from '@/api/catalog';

const state = {
  artists: [],
};

const getters = {
  // @ts-ignore
  artists: (state) => state.artists,
  // @ts-ignore
  artistByUid: (state) => (uid: string) => state.artists.find((obj) => obj.uid === uid),
};

const mutations = {
  // @ts-ignore
  SET_ARTIST: (state, { artist }) => {
  // @ts-ignore
    const index = state.artists.findIndex((obj) => obj.uid === artist.uid);
    if (index > -1) {
      state.artists[index] = artist;
    } else {
      state.artists.push(artist);
    }
  },
};

const actions = {
  // @ts-ignore
  loadArtist: async (context, uid: string) => {
    const artist = await getArtist(uid);
    context.commit('SET_ARTIST', { artist });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
